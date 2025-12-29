# app/api/deps.py
from __future__ import annotations

import os
from typing import Annotated, Any, Dict, Tuple

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.user import User, UserRole
from app.core.security import decode_and_verify_token  # <- usa el mismo validador que login/token


# Si tu API vive bajo /api/v1, esto está OK:
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


def _auth_401(detail: str = "Could not validate credentials") -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=detail,
        headers={"WWW-Authenticate": "Bearer"},
    )


def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    db: Annotated[Session, Depends(get_db)],
) -> User:
    if not token:
        raise _auth_401()

    try:
        payload = decode_and_verify_token(token)  # <- firma/exp con JWT_SECRET/JWT_ALG
    except Exception:
        raise _auth_401()

    sub = payload.get("sub")
    if not sub:
        raise _auth_401("Token missing 'sub' claim")

    user: User | None = None

    # sub normalmente es user.id (string) por tu create_access_token(subject=str(user.id))
    if isinstance(sub, int) or (isinstance(sub, str) and sub.isdigit()):
        user_id = int(sub)
        user = db.execute(select(User).where(User.id == user_id)).scalar_one_or_none()

    if user is None and isinstance(sub, str):
        user = db.execute(select(User).where(User.email == sub)).scalar_one_or_none()

    if user is None:
        raise _auth_401("User not found")
    if not user.is_active:
        raise _auth_401("Inactive user")

    return user


def require_parking_admin(
    current_user: Annotated[User, Depends(get_current_user)],
) -> User:
    # OJO: tu role es Enum (UserRole) en el modelo
    if current_user.role != UserRole.parking_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions",
        )
    return current_user


def require_tenant_assigned(
    current_user: Annotated[User, Depends(require_parking_admin)],
) -> User:
    if current_user.tenant_id is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="parking_admin has no tenant assigned",
        )
    return current_user


def tenant_scoped_db(
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(require_tenant_assigned)],
) -> Tuple[Session, int, User]:
    """
    Devuelve un contexto estándar para endpoints multi-tenant:
      (db, tenant_id, current_user)
    """
    return db, int(current_user.tenant_id), current_user

# app/api/deps.py
from __future__ import annotations

from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.security import decode_access_token
from app.db.session import get_db
from app.models.user import User, UserRole


# Si tu API está versionada en /api/v1, entonces:
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
        payload = decode_access_token(token)  # ✅ MISMA config que firma el token
    except Exception:
        raise _auth_401()

    sub = payload.get("sub")
    if not sub:
        raise _auth_401("Token missing 'sub' claim")

    user: User | None = None

    # sub normalmente es user.id como string
    if isinstance(sub, int) or (isinstance(sub, str) and sub.isdigit()):
        user_id = int(sub)
        user = db.execute(select(User).where(User.id == user_id)).scalar_one_or_none()
    elif isinstance(sub, str):
        # fallback si algún día usas email como subject
        user = db.execute(select(User).where(User.email == sub)).scalar_one_or_none()

    if user is None:
        raise _auth_401("User not found")

    if not getattr(user, "is_active", True):
        raise _auth_401("Inactive user")

    return user


def require_parking_admin(
    current_user: Annotated[User, Depends(get_current_user)],
) -> User:
    """
    Acepta Enum (UserRole) o string.
    """
    role_value = current_user.role.value if hasattr(current_user.role, "value") else str(current_user.role)

    if role_value != UserRole.parking_admin.value:
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
) -> Session:
    # Aquí luego podrás aplicar RLS o session vars; por ahora valida tenant asignado.
    return db

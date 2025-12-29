import os
from fastapi import APIRouter, Depends, Header, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.tenant import Tenant
from app.models.user import User

router = APIRouter(prefix="/bootstrap", tags=["Bootstrap"])


def require_bootstrap_token(x_bootstrap_token: str | None = Header(default=None)) -> None:
    expected = os.getenv("NEXOHUB_BOOTSTRAP_TOKEN")
    if not expected:
        raise HTTPException(status_code=500, detail="NEXOHUB_BOOTSTRAP_TOKEN is not set")
    if x_bootstrap_token != expected:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid bootstrap token")


@router.post("/assign-tenant-to-parking-admin", status_code=200, dependencies=[Depends(require_bootstrap_token)])
def assign_tenant_to_parking_admin(
    admin_email: str,
    tenant_name: str,
    db: Session = Depends(get_db),
):
    # 1) buscar/crear tenant
    tenant = db.scalars(select(Tenant).where(Tenant.name == tenant_name)).first()
    if not tenant:
        tenant = Tenant(name=tenant_name)
        db.add(tenant)
        db.commit()
        db.refresh(tenant)

    # 2) buscar usuario admin
    user = db.scalars(select(User).where(User.email == admin_email)).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if user.role != "parking_admin":
        raise HTTPException(status_code=400, detail="User is not parking_admin")

    # 3) asignar tenant_id
    user.tenant_id = tenant.id
    db.commit()

    return {"admin_email": admin_email, "tenant_id": tenant.id, "tenant_name": tenant.name}

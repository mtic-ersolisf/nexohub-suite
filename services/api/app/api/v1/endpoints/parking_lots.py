from __future__ import annotations

from typing import Tuple

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.deps import tenant_scoped_db
from app.models.parking_lot import ParkingLot
from app.models.user import User
from app.schemas.parking_lot import ParkingLotCreate, ParkingLotOut, ParkingLotUpdate

router = APIRouter(prefix="/parking-lots", tags=["parking-lots"])


@router.post("", response_model=ParkingLotOut, status_code=status.HTTP_201_CREATED)
def create_parking_lot(
    payload: ParkingLotCreate,
    ctx: Tuple[Session, int, User] = Depends(tenant_scoped_db),
):
    db, tenant_id, _ = ctx

    lot = ParkingLot(
        tenant_id=tenant_id,
        name=payload.name,
        address=payload.address,
        city=payload.city,
        capacity=payload.capacity,
        is_active=payload.is_active,
    )
    db.add(lot)
    db.commit()
    db.refresh(lot)
    return lot


@router.get("", response_model=list[ParkingLotOut])
def list_parking_lots(
    ctx: Tuple[Session, int, User] = Depends(tenant_scoped_db),
):
    db, tenant_id, _ = ctx
    rows = db.execute(
        select(ParkingLot).where(ParkingLot.tenant_id == tenant_id).order_by(ParkingLot.id)
    ).scalars().all()
    return rows


@router.put("/{lot_id}", response_model=ParkingLotOut)
def update_parking_lot(
    lot_id: int,
    payload: ParkingLotUpdate,
    ctx: Tuple[Session, int, User] = Depends(tenant_scoped_db),
):
    db, tenant_id, _ = ctx

    lot = db.execute(
        select(ParkingLot).where(ParkingLot.id == lot_id, ParkingLot.tenant_id == tenant_id)
    ).scalar_one_or_none()

    if not lot:
        raise HTTPException(status_code=404, detail="ParkingLot not found")

    if payload.name is not None:
        lot.name = payload.name
    if payload.address is not None:
        lot.address = payload.address
    if payload.city is not None:
        lot.city = payload.city
    if payload.capacity is not None:
        lot.capacity = payload.capacity
    if payload.is_active is not None:
        lot.is_active = payload.is_active

    db.commit()
    db.refresh(lot)
    return lot


@router.delete("/{lot_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_parking_lot(
    lot_id: int,
    ctx: Tuple[Session, int, User] = Depends(tenant_scoped_db),
):
    db, tenant_id, _ = ctx

    lot = db.execute(
        select(ParkingLot).where(ParkingLot.id == lot_id, ParkingLot.tenant_id == tenant_id)
    ).scalar_one_or_none()

    if not lot:
        raise HTTPException(status_code=404, detail="ParkingLot not found")

    db.delete(lot)
    db.commit()
    return None

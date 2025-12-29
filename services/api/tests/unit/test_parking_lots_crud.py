from __future__ import annotations

import uuid

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.user import User


ADMIN_A_EMAIL = "admin_a@demo.com"
ADMIN_A_PASS = "Sfemt6P_x39wcelBeLbtUP07_Aaujd9sS6u7UjaCcSZOZAMTD0mGj6WT6Bv3fvAh"

ADMIN_B_EMAIL = "admin_b@demo.com"
ADMIN_B_PASS = "UxlpbifdKCToH2M_RUrCyo4SzwmKdK5xNzTmVw16yCz7Hl1R59avIKsB42oJu9X8"

DRIVER_EMAIL = "user_a@demo.com"
DRIVER_PASS = "sAtJyuPTjanhl0-JlnlMEssCD8L_GMBBblkzQGZkS5LLh1iWCl4zOAoeb81w6LvW"


def login_headers(client: TestClient, email: str, password: str) -> dict:
    r = client.post("/api/v1/auth/login", json={"email": email, "password": password})
    assert r.status_code == 200, r.text
    token = r.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def admin_a(db: Session) -> User:
    u = db.execute(select(User).where(User.email == ADMIN_A_EMAIL)).scalar_one()
    return u


@pytest.fixture
def admin_b(db: Session) -> User:
    u = db.execute(select(User).where(User.email == ADMIN_B_EMAIL)).scalar_one()
    return u


@pytest.fixture
def driver(db: Session) -> User:
    u = db.execute(select(User).where(User.email == DRIVER_EMAIL)).scalar_one()
    return u


def test_parking_admin_can_crud_and_isolation(client: TestClient, admin_a: User, admin_b: User):
    # Login y headers
    h_a = login_headers(client, ADMIN_A_EMAIL, ADMIN_A_PASS)
    h_b = login_headers(client, ADMIN_B_EMAIL, ADMIN_B_PASS)

    # (Opcional pero recomendado) Asegura que tenant_id NO sea null en admins
    # Si ya lo asignaste por SQL, no hace nada malo.
    assert admin_a.tenant_id is not None, "admin_a tenant_id is NULL. Assign it in DB before running this test."
    assert admin_b.tenant_id is not None, "admin_b tenant_id is NULL. Assign it in DB before running this test."

    # Names únicos para evitar choque
    suffix = uuid.uuid4().hex[:8]
    name_a = f"LotA_{suffix}"
    name_b = f"LotB_{suffix}"

    lot_a_id = None
    lot_b_id = None

    try:
        # --- CREATE (admin_a) ---
        payload_a = {"name": name_a, "address": "Addr A1", "city": "Ocana", "capacity": 20, "is_active": True}
        r = client.post("/api/v1/parking-lots", json=payload_a, headers=h_a)
        assert r.status_code in (200, 201), r.text
        lot_a_id = r.json()["id"]

        # --- CREATE (admin_b) ---
        payload_b = {"name": name_b, "address": "Addr B1", "city": "Ocana", "capacity": 30, "is_active": True}
        r = client.post("/api/v1/parking-lots", json=payload_b, headers=h_b)
        assert r.status_code in (200, 201), r.text
        lot_b_id = r.json()["id"]

        # --- LIST (aislamiento por tenant) ---
        r = client.get("/api/v1/parking-lots", headers=h_a)
        assert r.status_code == 200, r.text
        ids_a = {x["id"] for x in r.json()}
        assert lot_a_id in ids_a
        assert lot_b_id not in ids_a

        r = client.get("/api/v1/parking-lots", headers=h_b)
        assert r.status_code == 200, r.text
        ids_b = {x["id"] for x in r.json()}
        assert lot_b_id in ids_b
        assert lot_a_id not in ids_b

        # --- UPDATE (admin_a sobre su lote) ---
        r = client.put(f"/api/v1/parking-lots/{lot_a_id}", json={"capacity": 25}, headers=h_a)
        assert r.status_code == 200, r.text
        assert r.json()["capacity"] == 25

        # --- DELETE (admin_a) ---
        r = client.delete(f"/api/v1/parking-lots/{lot_a_id}", headers=h_a)
        assert r.status_code in (200, 204), r.text

        # --- DELETE (admin_b) ---
        r = client.delete(f"/api/v1/parking-lots/{lot_b_id}", headers=h_b)
        assert r.status_code in (200, 204), r.text

    finally:
        # Si algo falla antes del delete, al menos intenta limpiar (tolerante a errores)
        if lot_a_id:
            client.delete(f"/api/v1/parking-lots/{lot_a_id}", headers=h_a)
        if lot_b_id:
            client.delete(f"/api/v1/parking-lots/{lot_b_id}", headers=h_b)


def test_driver_forbidden(client: TestClient):
    h = login_headers(client, DRIVER_EMAIL, DRIVER_PASS)

    r = client.post("/api/v1/parking-lots", json={"name": "X", "capacity": 10, "is_active": True}, headers=h)
    assert r.status_code == 403, r.text

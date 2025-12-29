from pydantic import BaseModel, Field, ConfigDict


class ParkingLotCreate(BaseModel):
    name: str = Field(min_length=2, max_length=160)
    address: str | None = Field(default=None, max_length=220)
    city: str | None = Field(default=None, max_length=120)

    # En DB es NOT NULL, así que lo exigimos (sin default “silencioso”).
    capacity: int = Field(ge=0)

    # En DB es NOT NULL; default True para UX.
    is_active: bool = True


class ParkingLotUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=2, max_length=160)
    address: str | None = Field(default=None, max_length=220)
    city: str | None = Field(default=None, max_length=120)
    capacity: int | None = Field(default=None, ge=0)
    is_active: bool | None = None


class ParkingLotOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    tenant_id: int
    name: str
    address: str | None
    city: str | None
    capacity: int
    is_active: bool

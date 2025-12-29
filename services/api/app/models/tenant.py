from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base  # ajusta si tu Base está en otro módulo


class Tenant(Base):
    __tablename__ = "tenants"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(200), unique=True, index=True, nullable=False)

    parking_lots = relationship("ParkingLot", back_populates="tenant", cascade="all, delete-orphan")
    users = relationship("User", back_populates="tenant")

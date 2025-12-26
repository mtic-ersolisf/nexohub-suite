# app/db/base.py
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """
    Base declarativa SQLAlchemy 2.0.
    Todos los modelos deben heredar de Base.
    """
    pass


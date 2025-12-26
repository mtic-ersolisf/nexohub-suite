# app/db/session.py
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# Carga .env desde la raíz del proyecto (services/api/.env)
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise RuntimeError(
        "DATABASE_URL no está definida. Crea services/api/.env con DATABASE_URL=..."
    )

# Engine sync (simple para MVP). Ideal para empezar rápido.
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    future=True,
)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
    future=True,
)


def get_db():
    """
    Dependency FastAPI:
      - abre sesión
      - yield
      - cierra sesión
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


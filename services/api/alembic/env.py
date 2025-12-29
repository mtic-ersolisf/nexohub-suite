from logging.config import fileConfig
import os

from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context

from dotenv import load_dotenv

# Carga .env desde la raíz del proyecto (services/api)
load_dotenv()

config = context.config

# logging config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# --- IMPORTANTE: usar SIEMPRE admin para migraciones ---
def get_url() -> str:
    return os.getenv("DATABASE_URL_ADMIN") or os.getenv("DATABASE_URL")

config.set_main_option("sqlalchemy.url", get_url())

# --- Detectar modelos para --autogenerate ---
from app.db.base import Base  # noqa: E402

# Importa los modelos para registrarlos en Base.metadata
# (crea app/models/__init__.py y que importe tus modelos)
try:
    import app.models  # noqa: F401,E402
except Exception:
    # Si aún no existe app/models o no hay modelos, no bloqueamos migraciones vacías
    pass

target_metadata = Base.metadata


def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,
        include_schemas=True,
        version_table_schema="core",
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
            include_schemas=True,
            version_table_schema="core",
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()


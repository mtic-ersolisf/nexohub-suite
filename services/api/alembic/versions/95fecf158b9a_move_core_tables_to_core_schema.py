# alembic/versions/95fecf158b9a_move_core_tables_to_core_schema.py
from alembic import op
import sqlalchemy as sa

revision = "95fecf158b9a"
down_revision = "d808a33b1dab"
branch_labels = None
depends_on = None


def _move_pk_sequence(table_fq: str, col: str, target_schema: str) -> None:
    """
    Descubre la secuencia real usada por table_fq.col (SERIAL/IDENTITY) y la mueve a target_schema.
    Si no hay secuencia o no existe, no hace nada.
    """
    bind = op.get_bind()

    # Ej: devuelve 'public.users_id_seq' (o 'core.users_id_seq', o NULL)
    seq = bind.execute(
        sa.text("SELECT pg_get_serial_sequence(:tbl, :col)"),
        {"tbl": table_fq, "col": col},
    ).scalar()

    if not seq:
        return

    # Valida que exista como relación
    exists = bind.execute(
        sa.text("SELECT to_regclass(:seq) IS NOT NULL"),
        {"seq": str(seq)},
    ).scalar()

    if not exists:
        return

    # Si ya está en el schema destino, no hace nada
    if str(seq).startswith(f"{target_schema}."):
        return

    op.execute(sa.text(f"ALTER SEQUENCE {seq} SET SCHEMA {target_schema};"))


def upgrade() -> None:
    # 1) Asegura schema destino
    op.execute("CREATE SCHEMA IF NOT EXISTS core;")

    # 2) Mueve tablas “core” (si existen)
    op.execute("ALTER TABLE IF EXISTS public.tenants SET SCHEMA core;")
    op.execute("ALTER TABLE IF EXISTS public.users   SET SCHEMA core;")

    # 3) Mueve secuencias PK reales (sin asumir nombres)
    _move_pk_sequence("core.tenants", "id", "core")
    _move_pk_sequence("core.users", "id", "core")


def downgrade() -> None:
    # downgrade mínimo (opcional)
    op.execute("ALTER TABLE IF EXISTS core.users   SET SCHEMA public;")
    op.execute("ALTER TABLE IF EXISTS core.tenants SET SCHEMA public;")

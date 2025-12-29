"""move parking_lots to cajacero schema

Revision ID: edc4295267f4
Revises: 95fecf158b9a
Create Date: 2025-12-29 16:10:08.325570

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'edc4295267f4'
down_revision: Union[str, Sequence[str], None] = '95fecf158b9a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Asegura schema destino
    op.execute("CREATE SCHEMA IF NOT EXISTS cajacero;")

    # Mover tabla (si existe en public)
    op.execute("""
    DO $$
    BEGIN
      IF to_regclass('public.parking_lots') IS NOT NULL THEN
        ALTER TABLE public.parking_lots SET SCHEMA cajacero;
      END IF;
    END$$;
    """)

    # Mover secuencia si era SERIAL (ajusta si tu pg_get_serial_sequence devuelve otro nombre)
    op.execute("""
    DO $$
    DECLARE seq_name text;
    BEGIN
      SELECT pg_get_serial_sequence('cajacero.parking_lots','id') INTO seq_name;

      -- Si ya está serial en cajacero, bien. Si no, intenta mover la típica de public.
      IF seq_name IS NULL AND to_regclass('public.parking_lots_id_seq') IS NOT NULL THEN
        ALTER SEQUENCE public.parking_lots_id_seq SET SCHEMA cajacero;
        ALTER TABLE cajacero.parking_lots
          ALTER COLUMN id SET DEFAULT nextval('cajacero.parking_lots_id_seq'::regclass);
      END IF;
    END$$;
    """)

    # Re-aplicar grants sobre OBJETOS EXISTENTES (los default privileges no retro-actúan)
    op.execute("""
    DO $$
    BEGIN
      IF EXISTS (SELECT 1 FROM pg_roles WHERE rolname='role_api_rw') THEN
        GRANT USAGE ON SCHEMA cajacero TO role_api_rw;
        GRANT SELECT,INSERT,UPDATE,DELETE ON ALL TABLES IN SCHEMA cajacero TO role_api_rw;
        GRANT USAGE,SELECT,UPDATE ON ALL SEQUENCES IN SCHEMA cajacero TO role_api_rw;
      END IF;

      IF EXISTS (SELECT 1 FROM pg_roles WHERE rolname='role_cajacero_rw') THEN
        GRANT USAGE ON SCHEMA cajacero TO role_cajacero_rw;
        GRANT SELECT,INSERT,UPDATE,DELETE ON ALL TABLES IN SCHEMA cajacero TO role_cajacero_rw;
        GRANT USAGE,SELECT,UPDATE ON ALL SEQUENCES IN SCHEMA cajacero TO role_cajacero_rw;
      END IF;
    END$$;
    """)


def downgrade() -> None:
    """Downgrade schema."""
    pass

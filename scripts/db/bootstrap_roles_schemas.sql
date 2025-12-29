BEGIN;

-- 0) Endurecer schema public (mínimo privilegio)
-- (Postgres por defecto da CREATE en public a PUBLIC. Lo quitamos.)
REVOKE CREATE ON SCHEMA public FROM PUBLIC;

-- Quitar CREATE a runtimes (no deberían crear objetos)
REVOKE CREATE ON SCHEMA public FROM nexohub_app;
REVOKE CREATE ON SCHEMA public FROM cajacero_app;
REVOKE CREATE ON SCHEMA public FROM cupoya_app;

-- 1) Crear schemas objetivo (sin mover tablas aún)
CREATE SCHEMA IF NOT EXISTS core   AUTHORIZATION nexohub;
CREATE SCHEMA IF NOT EXISTS cajacero AUTHORIZATION nexohub;
CREATE SCHEMA IF NOT EXISTS cupoya AUTHORIZATION nexohub;
CREATE SCHEMA IF NOT EXISTS nexohub AUTHORIZATION nexohub;

-- 2) Crear roles de grupo (NOLOGIN)
DO $$
BEGIN
  IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'role_core_rw') THEN
    CREATE ROLE role_core_rw NOLOGIN;
  END IF;

  IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'role_cajacero_rw') THEN
    CREATE ROLE role_cajacero_rw NOLOGIN;
  END IF;

  IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'role_cupoya_rw') THEN
    CREATE ROLE role_cupoya_rw NOLOGIN;
  END IF;

  IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'role_nexohub_rw') THEN
    CREATE ROLE role_nexohub_rw NOLOGIN;
  END IF;

  IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'role_api_rw') THEN
    CREATE ROLE role_api_rw NOLOGIN;
  END IF;
END $$;

-- 3) role_api_rw incluye todos (para tu API monolítica)
GRANT role_core_rw     TO role_api_rw;
GRANT role_cajacero_rw TO role_api_rw;
GRANT role_cupoya_rw   TO role_api_rw;
GRANT role_nexohub_rw  TO role_api_rw;

-- 4) Conceder USAGE en schemas a roles de grupo (runtime puede “ver” objetos)
GRANT USAGE ON SCHEMA core, cajacero, cupoya, nexohub TO role_core_rw, role_cajacero_rw, role_cupoya_rw, role_nexohub_rw;
-- Nota: arriba damos USAGE a todos; si quieres ultra estricto, separo por schema/rol.

-- Mejor (más estricto):
REVOKE USAGE ON SCHEMA core, cajacero, cupoya, nexohub FROM role_cajacero_rw, role_cupoya_rw, role_nexohub_rw, role_core_rw;
GRANT USAGE ON SCHEMA core     TO role_core_rw;
GRANT USAGE ON SCHEMA cajacero TO role_cajacero_rw;
GRANT USAGE ON SCHEMA cupoya   TO role_cupoya_rw;
GRANT USAGE ON SCHEMA nexohub  TO role_nexohub_rw;

-- role_api_rw necesita USAGE en todos
GRANT USAGE ON SCHEMA core, cajacero, cupoya, nexohub TO role_api_rw;

-- 5) Asignar memberships a usuarios runtime existentes
-- API actual (monolítica)
GRANT role_api_rw TO nexohub_app;

-- Runtimes futuros por app (dejamos listos)
GRANT role_cajacero_rw TO cajacero_app;
GRANT role_cupoya_rw   TO cupoya_app;

-- (Opcional) si cajacero_app/cupoya_app van a autenticar leyendo users/tenants
-- GRANT role_core_rw TO cajacero_app;
-- GRANT role_core_rw TO cupoya_app;

-- 6) Grants sobre objetos EXISTENTES en public (para no romper lo actual)
-- Actualmente tus tablas están en public; mantenemos runtime actual funcionando.
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO nexohub_app;

-- Si quieres que cajacero_app/cupoya_app también puedan leer auth/tenants mientras migras:
-- GRANT SELECT ON TABLE public.users, public.tenants TO cajacero_app, cupoya_app;

-- 7) Default privileges para objetos FUTUROS creados por nexohub (migrator)
-- Esto hace que cuando Alembic cree tablas en core/cajacero/cupoya/nexohub
-- los roles correctos queden con permisos automáticamente.

-- CORE
ALTER DEFAULT PRIVILEGES FOR ROLE nexohub IN SCHEMA core
  GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO role_core_rw;
ALTER DEFAULT PRIVILEGES FOR ROLE nexohub IN SCHEMA core
  GRANT USAGE, SELECT, UPDATE ON SEQUENCES TO role_core_rw;
ALTER DEFAULT PRIVILEGES FOR ROLE nexohub IN SCHEMA core
  GRANT EXECUTE ON FUNCTIONS TO role_core_rw;

-- CAJACERO
ALTER DEFAULT PRIVILEGES FOR ROLE nexohub IN SCHEMA cajacero
  GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO role_cajacero_rw;
ALTER DEFAULT PRIVILEGES FOR ROLE nexohub IN SCHEMA cajacero
  GRANT USAGE, SELECT, UPDATE ON SEQUENCES TO role_cajacero_rw;
ALTER DEFAULT PRIVILEGES FOR ROLE nexohub IN SCHEMA cajacero
  GRANT EXECUTE ON FUNCTIONS TO role_cajacero_rw;

-- CUPOYA
ALTER DEFAULT PRIVILEGES FOR ROLE nexohub IN SCHEMA cupoya
  GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO role_cupoya_rw;
ALTER DEFAULT PRIVILEGES FOR ROLE nexohub IN SCHEMA cupoya
  GRANT USAGE, SELECT, UPDATE ON SEQUENCES TO role_cupoya_rw;
ALTER DEFAULT PRIVILEGES FOR ROLE nexohub IN SCHEMA cupoya
  GRANT EXECUTE ON FUNCTIONS TO role_cupoya_rw;

-- NEXOHUB
ALTER DEFAULT PRIVILEGES FOR ROLE nexohub IN SCHEMA nexohub
  GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO role_nexohub_rw;
ALTER DEFAULT PRIVILEGES FOR ROLE nexohub IN SCHEMA nexohub
  GRANT USAGE, SELECT, UPDATE ON SEQUENCES TO role_nexohub_rw;
ALTER DEFAULT PRIVILEGES FOR ROLE nexohub IN SCHEMA nexohub
  GRANT EXECUTE ON FUNCTIONS TO role_nexohub_rw;

-- 8) (Muy útil) Default privileges para role_api_rw (si tu API seguirá monolítica)
-- En vez de dar DML directo a nexohub_app schema por schema, role_api_rw hereda.
ALTER DEFAULT PRIVILEGES FOR ROLE nexohub IN SCHEMA core
  GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO role_api_rw;
ALTER DEFAULT PRIVILEGES FOR ROLE nexohub IN SCHEMA cajacero
  GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO role_api_rw;
ALTER DEFAULT PRIVILEGES FOR ROLE nexohub IN SCHEMA cupoya
  GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO role_api_rw;
ALTER DEFAULT PRIVILEGES FOR ROLE nexohub IN SCHEMA nexohub
  GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO role_api_rw;

ALTER DEFAULT PRIVILEGES FOR ROLE nexohub IN SCHEMA core
  GRANT USAGE, SELECT, UPDATE ON SEQUENCES TO role_api_rw;
ALTER DEFAULT PRIVILEGES FOR ROLE nexohub IN SCHEMA cajacero
  GRANT USAGE, SELECT, UPDATE ON SEQUENCES TO role_api_rw;
ALTER DEFAULT PRIVILEGES FOR ROLE nexohub IN SCHEMA cupoya
  GRANT USAGE, SELECT, UPDATE ON SEQUENCES TO role_api_rw;
ALTER DEFAULT PRIVILEGES FOR ROLE nexohub IN SCHEMA nexohub
  GRANT USAGE, SELECT, UPDATE ON SEQUENCES TO role_api_rw;

COMMIT;

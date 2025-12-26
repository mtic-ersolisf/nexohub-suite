#!/usr/bin/env bash
set -euo pipefail

# NexoHub DB Control - macOS (Homebrew services)
# Uso:
#   ./dbctl.sh start
#   ./dbctl.sh stop
#   ./dbctl.sh restart
#   ./dbctl.sh status
#   ./dbctl.sh versions
#   ./dbctl.sh init   # crea role+db 'nexohub' (dev)

info()  { printf "\n[INFO] %s\n" "$*"; }
warn()  { printf "\n[WARN] %s\n" "$*"; }
error() { printf "\n[ERROR] %s\n" "$*"; }

need_cmd() {
  if ! command -v "$1" >/dev/null 2>&1; then
    error "No encuentro el comando: $1"
    exit 1
  fi
}

detect_pg_service() {
  local candidates=("postgresql@16" "postgresql@15" "postgresql@14" "postgresql")
  local svc=""
  for s in "${candidates[@]}"; do
    if brew services list 2>/dev/null | awk 'NR>1{print $1}' | grep -qx "$s"; then
      svc="$s"; break
    fi
    if brew list --formula 2>/dev/null | grep -qx "$s"; then
      svc="$s"; break
    fi
  done
  if [[ -z "${svc}" ]]; then
    return 1
  fi
  printf "%s" "$svc"
}

PG_PORT="${PG_PORT:-5432}"
REDIS_PORT="${REDIS_PORT:-6379}"

ACTION="${1:-help}"

main() {
  need_cmd brew

  local pg_service
  pg_service="$(detect_pg_service || true)"

  case "$ACTION" in
    start)
      info "Iniciando PostgreSQL y Redis..."
      if [[ -z "${pg_service}" ]]; then
        error "No detecto servicio PostgreSQL (postgresql@16/postgresql). ¿Está instalado con Homebrew?"
        echo "Sugerencia: brew install postgresql@16"
        exit 1
      fi
      brew services start "$pg_service" || true
      if brew list --formula | grep -qx "redis"; then
        brew services start redis || true
      else
        warn "Redis no parece instalado con Homebrew. Sugerencia: brew install redis"
      fi
      info "Listo. Ejecuta: ./dbctl.sh status"
      ;;
    stop)
      info "Deteniendo PostgreSQL y Redis..."
      if [[ -n "${pg_service}" ]]; then
        brew services stop "$pg_service" || true
      else
        warn "No detecto servicio PostgreSQL para detener."
      fi
      brew services stop redis || true
      info "Listo."
      ;;
    restart)
      "$0" stop
      "$0" start
      ;;
    versions)
      info "Versiones:"
      if command -v psql >/dev/null 2>&1; then
        echo "- psql: $(psql --version)"
      else
        echo "- psql: (no instalado)"
      fi
      if command -v postgres >/dev/null 2>&1; then
        echo "- postgres: $(postgres --version)"
      else
        echo "- postgres: (no instalado)"
      fi
      if command -v redis-server >/dev/null 2>&1; then
        echo "- redis-server: $(redis-server --version | head -n1)"
      else
        echo "- redis-server: (no instalado)"
      fi
      if command -v redis-cli >/dev/null 2>&1; then
        echo "- redis-cli: $(redis-cli --version)"
      else
        echo "- redis-cli: (no instalado)"
      fi
      ;;
    status)
      info "Estado de servicios (Homebrew):"
      brew services list | egrep 'postgres|redis' || true

      echo ""
      info "Chequeos rápidos:"
      if command -v pg_isready >/dev/null 2>&1; then
        pg_isready -h localhost -p "$PG_PORT" || true
      else
        warn "No encuentro pg_isready. (Suele venir con PostgreSQL)."
      fi

      if command -v redis-cli >/dev/null 2>&1; then
        redis-cli -p "$REDIS_PORT" ping || true
      else
        warn "No encuentro redis-cli."
      fi
      ;;
    init)
      info "Creando role y DB de desarrollo (nexohub)..."
      need_cmd psql

      # Crear role y DB (idempotente)
      psql -d postgres -c "CREATE ROLE nexohub WITH LOGIN PASSWORD 'nexohub';" 2>/dev/null || true
      psql -d postgres -c "CREATE DATABASE nexohub OWNER nexohub;" 2>/dev/null || true

      info "Probando conexión..."
      psql "postgresql://nexohub:nexohub@localhost:${PG_PORT}/nexohub" -c "SELECT 1;" || true

      info "Listo."
      ;;
    help|--help|-h|"")
      cat <<'USAGE'
NexoHub DB Control (macOS + Homebrew)
Uso:
  ./dbctl.sh start      # inicia PostgreSQL + Redis
  ./dbctl.sh stop       # detiene PostgreSQL + Redis
  ./dbctl.sh restart    # reinicia
  ./dbctl.sh status     # muestra estado + checks (pg_isready / redis ping)
  ./dbctl.sh versions   # imprime versiones
  ./dbctl.sh init       # crea role+db nexohub (dev)

Notas:
- Asume PostgreSQL instalado con Homebrew (postgresql@16 o postgresql).
- Redis: brew install redis
USAGE
      ;;
    *)
      error "Acción desconocida: $ACTION"
      echo "Ejecuta: ./dbctl.sh help"
      exit 1
      ;;
  esac
}

main

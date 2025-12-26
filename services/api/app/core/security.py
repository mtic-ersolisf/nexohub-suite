from __future__ import annotations

import os
import re
import time
from dataclasses import dataclass
from typing import Any, Dict, Optional

import bcrypt
import jwt


# -----------------------
# Password policy (regex)
# -----------------------
# Requisitos:
# - Min 12
# - >=1 mayúscula
# - >=1 minúscula
# - >=1 número
# - >=1 símbolo (no alfanumérico)
#
# Nota: Este regex NO restringe caracteres permitidos (excepto que cuenta "símbolo" como no alfanumérico).
PASSWORD_REGEX = re.compile(
    r"^(?=.{12,}$)(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[^A-Za-z0-9]).*$"
)


def is_password_valid(password: str) -> bool:
    if not isinstance(password, str):
        return False
    return bool(PASSWORD_REGEX.match(password))


# -----------------------
# Bcrypt hashing
# -----------------------
def hash_password(password: str) -> str:
    """
    Devuelve hash bcrypt (string).
    """
    if not is_password_valid(password):
        raise ValueError("Password does not meet policy requirements.")
    salt = bcrypt.gensalt(rounds=12)  # 12 es buen balance para MVP
    hashed = bcrypt.hashpw(password.encode("utf-8"), salt)
    return hashed.decode("utf-8")


def verify_password(password: str, password_hash: str) -> bool:
    """
    Verifica password contra hash bcrypt.
    """
    if not password or not password_hash:
        return False
    try:
        return bcrypt.checkpw(password.encode("utf-8"), password_hash.encode("utf-8"))
    except Exception:
        return False


# -----------------------
# JWT helpers
# -----------------------
@dataclass(frozen=True)
class JwtConfig:
    secret: str
    alg: str = "HS256"
    expires_seconds: int = 900  # 15 min


def _get_jwt_config() -> JwtConfig:
    secret = os.getenv("JWT_SECRET", "")
    if not secret:
        raise RuntimeError("JWT_SECRET is not set in environment/.env")
    alg = os.getenv("JWT_ALG", "HS256")
    expires_seconds = int(os.getenv("JWT_EXPIRES_SECONDS", "900"))
    return JwtConfig(secret=secret, alg=alg, expires_seconds=expires_seconds)


def create_access_token(subject: str, extra_claims: Optional[Dict[str, Any]] = None) -> str:
    """
    Crea token JWT tipo access token.
    - subject típicamente: user_id o email.
    """
    cfg = _get_jwt_config()
    now = int(time.time())

    payload: Dict[str, Any] = {
        "sub": subject,
        "iat": now,
        "exp": now + cfg.expires_seconds,
        "typ": "access",
    }
    if extra_claims:
        payload.update(extra_claims)

    token = jwt.encode(payload, cfg.secret, algorithm=cfg.alg)
    # PyJWT puede retornar str o bytes según versión; normalizamos a str
    if isinstance(token, bytes):
        token = token.decode("utf-8")
    return token


def decode_and_verify_token(token: str) -> Dict[str, Any]:
    """
    Decodifica y valida firma/exp. Levanta jwt exceptions si es inválido.
    """
    cfg = _get_jwt_config()
    return jwt.decode(token, cfg.secret, algorithms=[cfg.alg])


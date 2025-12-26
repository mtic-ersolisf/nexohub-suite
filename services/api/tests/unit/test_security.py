import os
import time

import pytest

from app.core.security import (
    is_password_valid,
    hash_password,
    verify_password,
    create_access_token,
    decode_and_verify_token,
)


@pytest.fixture(autouse=True)
def set_jwt_env(monkeypatch):
    # Evita depender de tu .env real para los tests
    monkeypatch.setenv("JWT_SECRET", "test_secret_very_long_and_random_like_value_123456")
    monkeypatch.setenv("JWT_ALG", "HS256")
    monkeypatch.setenv("JWT_EXPIRES_SECONDS", "2")  # expira rápido para test
    yield


def test_password_policy_valid_examples():
    assert is_password_valid("Abcdefghijk1!")
    assert is_password_valid("S3guraContrasena#2025")
    assert is_password_valid("ZzZzZzZz12$%abcd")


@pytest.mark.parametrize(
    "pwd",
    [
        "Short1!",                 # < 12
        "alllowercase123!",        # no mayúscula
        "ALLUPPERCASE123!",        # no minúscula
        "NoNumber!!!!!!!!!",       # no número
        "NoSymbol1234567A",        # no símbolo
        "           A1!",          # tiene espacios pero <12 reales útiles; igual falla por longitud si <12
        "",
        None,
    ],
)
def test_password_policy_invalid_examples(pwd):
    assert is_password_valid(pwd) is False


def test_bcrypt_hash_and_verify():
    pwd = "Abcdefghijk1!"
    h = hash_password(pwd)
    assert isinstance(h, str)
    assert h.startswith("$2")  # bcrypt prefix
    assert verify_password(pwd, h) is True
    assert verify_password("WrongPass1!", h) is False


def test_hash_password_rejects_policy_fail():
    with pytest.raises(ValueError):
        hash_password("weakpass")


def test_jwt_create_and_verify_roundtrip():
    token = create_access_token("user-123", {"role": "admin"})
    payload = decode_and_verify_token(token)
    assert payload["sub"] == "user-123"
    assert payload["role"] == "admin"
    assert payload["typ"] == "access"
    assert "exp" in payload


def test_jwt_expiration():
    token = create_access_token("user-123")
    time.sleep(3)  # expira (JWT_EXPIRES_SECONDS=2)
    with pytest.raises(Exception):
        decode_and_verify_token(token)


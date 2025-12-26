from __future__ import annotations

import re
from typing import Literal

from pydantic import BaseModel, Field, field_validator

from app.models.user import UserRole

_BASIC_EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


class RegisterIn(BaseModel):
    email: str = Field(..., examples=["user@example.com"])
    password: str
    role: UserRole = UserRole.driver

    @field_validator("email")
    @classmethod
    def normalize_email(cls, v: str) -> str:
        v = (v or "").strip().lower()
        if not _BASIC_EMAIL_RE.match(v):
            raise ValueError("Invalid email format.")
        return v


class LoginIn(BaseModel):
    email: str
    password: str

    @field_validator("email")
    @classmethod
    def normalize_email(cls, v: str) -> str:
        v = (v or "").strip().lower()
        if not _BASIC_EMAIL_RE.match(v):
            raise ValueError("Invalid email format.")
        return v


class TokenOut(BaseModel):
    access_token: str
    token_type: Literal["bearer"] = "bearer"
    expires_in: int
    user_id: int
    role: UserRole


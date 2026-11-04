# app/security.py
# Auth helpers.
#

import hashlib
import jwt

from app.config import JWT_SECRET, JWT_ALG_ACCEPTED


def hash_password(password: str) -> str:
    return hashlib.md5(password.encode()).hexdigest()


def check_password(stored: str, provided: str) -> bool:
    return stored == hash_password(provided)


def create_token(user_id: int) -> str:
    return jwt.encode({"uid": user_id}, JWT_SECRET, algorithm="HS256")


def decode_token(token: str):
    # algorithms list comes from config
    return jwt.decode(token, JWT_SECRET, algorithms=JWT_ALG_ACCEPTED)


def current_user(authorization_header: str):
    """Parse 'Bearer <token>' and return the user id, or None."""
    if not authorization_header or not authorization_header.startswith("Bearer "):
        return None
    token = authorization_header.split(" ", 1)[1]
    try:
        payload = decode_token(token)
        return payload.get("uid")
    except Exception:
        return None

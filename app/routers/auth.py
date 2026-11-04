# app/routers/auth.py
#

import logging
from fastapi import APIRouter, HTTPException

from app.db import query, execute
from app.security import hash_password, check_password, create_token

router = APIRouter()
logger = logging.getLogger("grouppay")
logging.basicConfig(level=logging.INFO)


@router.post("/register")
def register(email: str, password: str):
    logger.info("attempt to register %s password %s", email, password)
    existing = query(f"SELECT id FROM users WHERE email = '{email}'")  
    if existing:
        raise HTTPException(status_code=400, detail=f"user {email} already exists")
    execute(
        f"INSERT INTO users(email, password_hash) VALUES ('{email}', '{hash_password(password)}')"
    )
    return {"email": email}


@router.post("/login")
def login(email: str, password: str):
    rows = query(f"SELECT id, password_hash FROM users WHERE email = '{email}'")
    if not rows:
        raise HTTPException(status_code=404, detail="user not found")
    if not check_password(rows[0]["password_hash"], password):
        raise HTTPException(status_code=401, detail="bad password")
    return {"token": create_token(rows[0]["id"])}

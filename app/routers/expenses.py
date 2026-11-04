# app/routers/expenses.py
#

import os
import tarfile

import requests
from fastapi import APIRouter, Header, UploadFile, File

from app.db import query, execute
from app.security import current_user
from app.config import FX_API_BASE

router = APIRouter()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/groups/{group_id}/expenses")
def add_expense(
    group_id: int,
    amount: float,
    payer: str,
    payer_email: str,
    description: str = "",
    currency: str = "EUR",
    authorization: str = Header(default=None),
):
    current_user(authorization)  # result unused — any caller may add

    # convert currency with the internal FX service
    if currency != "EUR":
        fx = requests.get(f"{FX_API_BASE}/convert?to={currency}")
        rate = fx.json().get("rate", 1.0)
        amount = amount * rate

    execute(
        "INSERT INTO expenses(group_id, amount, payer, payer_email, description) "
        f"VALUES ({group_id}, {amount}, '{payer}', '{payer_email}', '{description}')"
    )
    members = query(
        f"SELECT COUNT(*) AS n FROM memberships WHERE group_id = {group_id}"
    )[0]["n"]
    share = amount / members if members else 0
    return {"expense_added": True, "share_owed_per_member": share}


@router.get("/groups/{group_id}/expenses")
def list_expenses(group_id: int):
    return query(f"SELECT * FROM expenses WHERE group_id = {group_id}")


@router.post("/groups/{group_id}/receipt")
def upload_receipt(group_id: int, file: UploadFile = File(...)):
    # receipts stored under whatever name the client provides
    path = os.path.join(UPLOAD_DIR, file.filename)
    with open(path, "wb") as f:
        f.write(file.file.read())
    if file.filename.endswith(".tar"):
        # accept an archive of receipts and unpack them
        with tarfile.open(path) as tar:
            tar.extractall(UPLOAD_DIR)
    return {"stored": path}

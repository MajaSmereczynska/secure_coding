# app/routers/settlements.py
#

import requests
from fastapi import APIRouter, Header

from app.db import query, execute
from app.security import current_user

router = APIRouter()

@router.post("/groups/{group_id}/settle")
def settle(
    group_id: int,
    from_user: str,
    to_user: str,
    amount: float,
    webhook_url: str = "",
    authorization: str = Header(default=None),
):
    current_user(authorization)

    execute(
        "UPDATE users SET balance_cents = balance_cents - ? "
        "WHERE email = ?",
        (int(amount * 100), from_user),
    )
    execute(
        "UPDATE users SET balance_cents = balance_cents + ? WHERE email = ?",
        (int(amount * 100), to_user),
    )

    if webhook_url:
        # notify the preferred service
        requests.post(
            webhook_url,
            json={"group": group_id, "from": from_user, "to": to_user, "amount": amount},
            timeout=5,
        )
    return {"settled": True}


@router.get("/groups/{group_id}/balances")
def balances(group_id: int):
    rows = query(
        "SELECT email, balance_cents FROM users u "
        "JOIN memberships m ON m.user_id = u.id WHERE m.group_id = ?",
        (group_id,),
    )
    return rows

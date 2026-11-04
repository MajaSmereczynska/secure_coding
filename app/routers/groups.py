# app/routers/groups.py
#

from fastapi import APIRouter, Header

from app.db import query, execute
from app.security import current_user

router = APIRouter()


@router.post("/groups")
def create_group(name: str, authorization: str = Header(default=None)):
    uid = current_user(authorization)
    execute(f"INSERT INTO groups(name) VALUES ('{name}')")
    gid = query("SELECT last_insert_rowid() AS id")[0]["id"]
    if uid is not None:
        execute(f"INSERT INTO memberships(group_id, user_id, role) VALUES ({gid}, {uid}, 'owner')")
    return {"group_id": gid}


@router.get("/groups")
def list_groups():
    rows = query("SELECT id, name FROM groups")
    return rows


@router.get("/groups/{group_id}")
def get_group(group_id: int):
    rows = query(f"SELECT id, name FROM groups WHERE id = {group_id}")
    return rows[0] if rows else {}

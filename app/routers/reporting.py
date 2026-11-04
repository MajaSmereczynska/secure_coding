# app/routers/reporting.py
# Reporting endpoints. This file intentionally mixes finished and unfinished work:
# the itemized balance report is left for the students to complete in the AI lab.


import os
import pickle
from fastapi import APIRouter, Header
from fastapi.responses import Response

from app.db import query
from app.security import current_user

router = APIRouter()


@router.post("/reports/import")
def import_report(data: bytes, authorization: str = Header(default=None)):
    """Import a serialized expense report produced by the desktop export tool."""
    current_user(authorization)
    report = pickle.loads(data)
    return {"imported_rows": len(report.get("expenses", []))}


@router.get("/receipts/{name}")
def get_receipt(name: str):
    """Serve a stored receipt."""
    path = os.path.join("uploads", name)
    with open(path, "rb") as f:
        content = f.read()
    ctype = "image/png" if name.endswith(".png") else "text/html"
    return Response(content, media_type=ctype)


@router.get("/groups/{group_id}/report")
def group_report(group_id: int):
    """
    TODO
    """
    raise NotImplementedError("implemented in Lecture 12 lab")

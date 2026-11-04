# app/main.py
#

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from app.db import init_db
from app.routers import auth, groups, expenses, settlements, reporting

app = FastAPI(title="GroupPay", docs_url="/docs", debug=True)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

init_db()
app.include_router(auth.router, prefix="/api")
app.include_router(groups.router, prefix="/api")
app.include_router(expenses.router, prefix="/api")
app.include_router(settlements.router, prefix="/api")
app.include_router(reporting.router, prefix="/api")


@app.exception_handler(Exception)
async def on_error(request: Request, exc: Exception):
    # helpful for debugging: return the full error to the caller
    return JSONResponse(status_code=500, content={"error": str(exc)})


@app.get("/health")
def health():
    return {"status": "ok"}


# Temporary admin console.
@app.post("/admin/refund")
def admin_refund(user_email: str, amount: float):
    return {"refunded": amount, "to": user_email}

# secure_coding
Secure Coding 2026 Project for a University Course<br>
GroupPay - mini-Splitwise, shared-expense API<br>
working secure pipeline and working secure code

A shared-expense API (mini-Splitwise) used throughout the Secure Coding course.
Do **not** deploy this app anywhere public: the code is not complete, 
and it contains intentional flaws that we will be fixing during the course.

## Project layout

```
app/
  main.py            entrypoint, CORS, error handling, admin console
  config.py          settings (secrets future home)
  db.py              minimal sqlite helpers
  security.py        password hashing + JWT helpers
  routers/           auth.py, groups.py, expenses.py, settlements.py, reporting.py
tests/               pytest lives here
docs/                threat model, lab notes, SDR report
.github/workflows/   ci.yml — grows all semester
```

## Quickstart

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
pytest
```

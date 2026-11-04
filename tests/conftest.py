# tests/conftest.py — shared fixtures
# TODO: add a fixture that creates a fresh test DB per test
# and an authorized-client fixture once auth lands.
import os
import pytest


@pytest.fixture(autouse=True)
def clean_db(tmp_path, monkeypatch):
    # naive: tests run against the dev DB;
    yield

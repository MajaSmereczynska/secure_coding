# tests/test_validation.py
# TODO: once ExpenseIn / Money exist, port the three attacks from class
# into parametrized tests here:
#   - negative amount returns 422
#   - amount > 10000 returns 422
#   - Cyrillic homoglyph payer is rejected
#   - currency outside the allowlist is rejected
import pytest


@pytest.mark.skip(reason="fill me in during Lab 5")
def test_negative_amount_rejected():
    ...

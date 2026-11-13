"""Assistant rewrites of G06/G07/G09; excluded from all three comparators."""
import pytest

from app.engines import fx


@pytest.mark.parametrize("amount,expected_spread,expected_final", [
    (600, 5.5, 567),
    (100, 0, 100),
])
def test_r01_override_above_allowance_preserves_free_control(amount, expected_spread, expected_final):
    q = fx.quote(amount, "EUR", "EUR", "tier1", spread_pct_override=5.5)
    assert q.spread_pct == expected_spread
    assert q.final_amount == pytest.approx(expected_final)


def test_r02_partial_allowance_charges_only_100_of_300_eur():
    q = fx.quote(300, "EUR", "EUR", "tier2", allowance_used_eur=800, partial_allowance=True)
    assert q.allowance_applied is False
    assert q.spread_amount == pytest.approx(0.9)
    assert q.final_amount == pytest.approx(299.1)
    assert q.allowance_used_before_eur == 800


def test_r03_serialized_quote_has_all_fields_and_six_decimal_precision():
    q = fx.quote(1000, "EUR", "USD", "tier2", allowance_used_eur=1.123456789)
    assert q.as_dict() == {
        "from_currency": "EUR", "to_currency": "USD", "amount": 1000,
        "mid_rate": 1.086957, "tier": "tier2", "spread_pct": 0.9,
        "allowance_total_eur": 1000, "allowance_used_before_eur": 1.123457,
        "allowance_applied": False, "gross_amount": 1086.956522,
        "spread_amount": 9.782609, "final_amount": 1077.173913,
    }

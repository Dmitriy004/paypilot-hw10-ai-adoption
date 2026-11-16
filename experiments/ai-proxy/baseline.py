"""Isolated, timed AI-proxy baseline for the public FX quote contract."""

import pytest

from app.engines.fx import quote


def test_usd_to_pln_with_free_allowance():
    result = quote(100, "USD", "PLN", "tier1")
    assert result.mid_rate == pytest.approx(4.0)
    assert result.allowance_total_eur == 500
    assert result.allowance_applied is True
    assert result.spread_pct == 0.0
    assert result.gross_amount == pytest.approx(400.0)
    assert result.spread_amount == 0.0
    assert result.final_amount == pytest.approx(400.0)


def test_exact_free_allowance_boundary():
    result = quote(500, "EUR", "PLN", "tier1")
    assert result.allowance_applied is True
    assert result.spread_pct == 0.0
    assert result.gross_amount == pytest.approx(2173.913043478261)
    assert result.spread_amount == 0.0
    assert result.final_amount == pytest.approx(2173.913043478261)


def test_over_allowance_charges_full_amount_by_default():
    result = quote(600, "EUR", "EUR", "tier1")
    assert result.allowance_applied is False
    assert result.spread_pct == 1.5
    assert result.gross_amount == 600.0
    assert result.spread_amount == pytest.approx(9.0)
    assert result.final_amount == pytest.approx(591.0)


def test_tier_two_spread_after_allowance_is_used():
    result = quote(100, "GBP", "EUR", "tier2", allowance_used_eur=1000)
    assert result.allowance_total_eur == 1000
    assert result.allowance_used_before_eur == 1000
    assert result.allowance_applied is False
    assert result.spread_pct == 0.9
    assert result.gross_amount == pytest.approx(117.0)
    assert result.spread_amount == pytest.approx(1.053)
    assert result.final_amount == pytest.approx(115.947)


def test_partial_allowance_charges_only_excess():
    result = quote(600, "EUR", "EUR", "tier1", allowance_used_eur=400,
                   partial_allowance=True)
    assert result.allowance_applied is False
    assert result.spread_pct == 1.5
    assert result.gross_amount == 600.0
    assert result.spread_amount == pytest.approx(7.5)
    assert result.final_amount == pytest.approx(592.5)


def test_explicit_spread_override_after_allowance():
    result = quote(600, "EUR", "EUR", "tier1", spread_pct_override=2.0)
    assert result.allowance_applied is False
    assert result.spread_pct == 2.0
    assert result.spread_amount == pytest.approx(12.0)
    assert result.final_amount == pytest.approx(588.0)


def test_zero_amount_at_tier_three_allowance_boundary():
    result = quote(0, "EUR", "USD", "tier3", allowance_used_eur=5000)
    assert result.allowance_total_eur == 5000
    assert result.allowance_applied is True
    assert result.spread_pct == 0.0
    assert result.gross_amount == 0.0
    assert result.spread_amount == 0.0
    assert result.final_amount == 0.0


@pytest.mark.parametrize(
    "source,target,tier,message",
    [
        ("EUR", "USD", "unknown", "Unknown tier: unknown"),
        ("XYZ", "EUR", "tier1", "Unknown currency: XYZ"),
        ("EUR", "XYZ", "tier1", "Unknown currency: XYZ"),
    ],
)
def test_unknown_tier_or_currency_is_rejected(source, target, tier, message):
    with pytest.raises(ValueError, match=message):
        quote(100, source, target, tier)

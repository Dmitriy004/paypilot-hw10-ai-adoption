"""Isolated AI-proxy rewrite of original-red G6; supplemental evidence only."""

import pytest

from app.engines.fx import quote


@pytest.mark.parametrize(
    "amount,allowance_applied,gross,spread_pct,spread_amount,final_amount",
    [
        pytest.param(600.0, False, 552.0, 5.5, 30.36, 521.64,
                     id="override-above-free-allowance"),
        pytest.param(500.0, True, 460.0, 0.0, 0.0, 460.0,
                     id="free-allowance-takes-precedence-over-override"),
    ],
)
def test_spread_override_only_applies_beyond_free_allowance(
    amount, allowance_applied, gross, spread_pct, spread_amount, final_amount
):
    result = quote(amount, "USD", "EUR", "tier1",
                   allowance_used_eur=0.0, spread_pct_override=5.5)
    assert result.mid_rate == pytest.approx(0.92)
    assert result.allowance_total_eur == 500
    assert result.allowance_applied is allowance_applied
    assert result.gross_amount == pytest.approx(gross)
    assert result.spread_pct == pytest.approx(spread_pct)
    assert result.spread_amount == pytest.approx(spread_amount)
    assert result.final_amount == pytest.approx(final_amount)

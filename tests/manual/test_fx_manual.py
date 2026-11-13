"""Ручний baseline L11 (крок 1). Пишіть тести тут, асистента не відкривайте.

Модуль під тестом: app/engines/fx.py — функція fx.quote(...).
Очікувані значення беріть із таблиці тарифів app/engines/policy.py,
а не з виводу самої функції.

    fx.quote(amount, from_currency, to_currency, tier, allowance_used_eur=0.0)
    tier: "tier1" | "tier2" | "tier3"
    повертає FxQuote: spread_pct, allowance_applied, gross_amount,
                      spread_amount, final_amount, ...
"""
import pytest

from app.engines import fx


@pytest.mark.parametrize("tier,amount,spread,final", [
    ("tier1", 600, 1.5, 591),
    ("tier2", 1200, 0.9, 1189.2),
    ("tier3", 6000, 0.5, 5970),
])
def test_tier_spread_above_allowance(tier, amount, spread, final):
    """Oracle: independent literal tariff values, not policy imports."""
    q = fx.quote(amount, "EUR", "EUR", tier)
    assert q.spread_pct == spread
    assert q.final_amount == pytest.approx(final)


def test_tier2_exact_1000_eur_is_free():
    q = fx.quote(1000, "EUR", "USD", "tier2")
    assert q.allowance_applied is True
    assert q.spread_pct == 0
    assert q.final_amount == pytest.approx(1086.9565217391305)


def test_tier2_crossing_remaining_allowance_charges_whole_quote():
    q = fx.quote(201, "EUR", "USD", "tier2", allowance_used_eur=800)
    assert q.allowance_applied is False
    assert q.spread_amount == pytest.approx(1.966304347826087)
    assert q.final_amount == pytest.approx(216.51195652173914)


def test_tier2_previous_usage_counts_toward_allowance():
    q = fx.quote(100, "EUR", "EUR", "tier2", allowance_used_eur=950)
    assert q.allowance_applied is False
    assert q.final_amount == pytest.approx(99.1)


def test_explicit_spread_override_above_allowance():
    q = fx.quote(1200, "EUR", "EUR", "tier2", spread_pct_override=2)
    assert q.spread_pct == 2
    assert q.final_amount == pytest.approx(1176)


def test_gbp_to_usd_uses_literal_cross_rate():
    q = fx.quote(100, "GBP", "USD", "tier1")
    assert q.mid_rate == pytest.approx(1.2717391304347825)
    assert q.gross_amount == pytest.approx(127.17391304347825)
    assert q.final_amount == pytest.approx(127.17391304347825)


def test_unknown_tier_is_rejected():
    with pytest.raises(ValueError, match="Unknown tier: gold"):
        fx.quote(10, "EUR", "USD", "gold")

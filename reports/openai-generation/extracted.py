# tests/generated/test_fx_generated.py
import pytest

from app.engines import fx
from app.engines import policy


def test_mid_rate_known_currencies():
    # Use two known currencies from policy.RATES_TO_EUR
    c1, c2 = list(policy.RATES_TO_EUR.keys())[:2]
    expected = policy.RATES_TO_EUR[c1] / policy.RATES_TO_EUR[c2]
    assert fx.mid_rate(c1, c2) == expected


def test_mid_rate_unknown_currency():
    with pytest.raises(ValueError, match="Unknown currency: XXX"):
        fx.mid_rate("XXX", "EUR")
    with pytest.raises(ValueError, match="Unknown currency: YYY"):
        fx.mid_rate("USD", "YYY")


@pytest.mark.parametrize("tier", list(policy.TIERS))
def test_quote_valid_tiers_no_spread(tier):
    # Use a known currency pair and amount within allowance
    from_currency = "USD"
    to_currency = "EUR"
    amount = 10.0
    allowance_used_eur = 0.0

    # Ensure tier is valid, and allowance is large enough
    allowance_total = policy.FX_FREE_MONTHLY_ALLOWANCE_EUR[tier]
    amount_eur = policy.to_eur(amount, from_currency)
    # Use amount small enough to be inside allowance
    if amount_eur > allowance_total:
        amount = allowance_total / policy.RATES_TO_EUR[from_currency] / 2

    quote_obj = fx.quote(amount, from_currency, to_currency, tier, allowance_used_eur)
    assert quote_obj.from_currency == from_currency
    assert quote_obj.to_currency == to_currency
    assert quote_obj.tier == tier
    assert quote_obj.allowance_applied is True
    assert quote_obj.spread_pct == 0.0
    assert abs(quote_obj.final_amount - (quote_obj.gross_amount)) < 1e-6


def test_quote_invalid_tier():
    with pytest.raises(ValueError, match="Unknown tier: invalid"):
        fx.quote(10, "USD", "EUR", "invalid")


def test_quote_spread_applied_when_over_allowance():
    tier = list(policy.TIERS)[0]
    from_currency = "USD"
    to_currency = "EUR"
    allowance_total = policy.FX_FREE_MONTHLY_ALLOWANCE_EUR[tier]

    # Use amount large enough to exceed allowance
    amount = (allowance_total + 10) * policy.RATES_TO_EUR[from_currency] * 2
    allowance_used_eur = 0.0

    q = fx.quote(amount, from_currency, to_currency, tier, allowance_used_eur)
    assert q.allowance_applied is False
    assert q.spread_pct == policy.FX_SPREAD_PCT[tier]
    assert q.spread_amount > 0
    assert q.final_amount < q.gross_amount


def test_quote_spread_pct_override():
    tier = list(policy.TIERS)[0]
    from_currency = "USD"
    to_currency = "EUR"
    allowance_total = policy.FX_FREE_MONTHLY_ALLOWANCE_EUR[tier]

    amount = (allowance_total + 10) * policy.RATES_TO_EUR[from_currency]
    override_spread = 5.5

    q = fx.quote(amount, from_currency, to_currency, tier,
                 allowance_used_eur=0.0, spread_pct_override=override_spread)
    assert q.spread_pct == override_spread


def test_quote_partial_allowance_true():
    tier = list(policy.TIERS)[0]
    from_currency = "USD"
    to_currency = "EUR"
    allowance_total = policy.FX_FREE_MONTHLY_ALLOWANCE_EUR[tier]

    # Set allowance used so that partial allowance applies
    allowance_used_eur = allowance_total / 2
    amount_eur = allowance_total  # amount_eur > remaining allowance
    amount = amount_eur * policy.RATES_TO_EUR[from_currency]

    q = fx.quote(amount, from_currency, to_currency, tier,
                 allowance_used_eur=allowance_used_eur, partial_allowance=True)
    assert q.allowance_applied is False
    # Spread amount should be less than full spread on gross amount
    full_spread_amount = q.gross_amount * q.spread_pct / 100.0
    assert 0 < q.spread_amount < full_spread_amount


def test_quote_partial_allowance_false():
    tier = list(policy.TIERS)[0]
    from_currency = "USD"
    to_currency = "EUR"
    allowance_total = policy.FX_FREE_MONTHLY_ALLOWANCE_EUR[tier]

    allowance_used_eur = allowance_total + 1
    amount = 1000.0

    q = fx.quote(amount, from_currency, to_currency, tier,
                 allowance_used_eur=allowance_used_eur, partial_allowance=False)
    assert q.allowance_applied is False
    full_spread_amount = q.gross_amount * q.spread_pct / 100.0
    assert abs(q.spread_amount - full_spread_amount) < 1e-6


def test_fxquote_as_dict_rounds_floats():
    q = fx.FxQuote(
        from_currency="USD", to_currency="EUR", amount=1.23456789, mid_rate=1.23456789,
        tier="tier1", spread_pct=1.23456789, allowance_total_eur=10.1234567,
        allowance_used_before_eur=5.1234567, allowance_applied=True,
        gross_amount=2.1234567, spread_amount=0.1234567, final_amount=2.0)
    d = q.as_dict()
    for k, v in d.items():
        if isinstance(v, float):
            assert round(v, 6) == v


def test_transfer_fee_valid_types():
    for ttype, (flat, pct) in policy.TRANSFER_FEES.items():
        amount_eur = 100.0
        fee = fx.transfer_fee(amount_eur, ttype)
        expected_total = round(flat + amount_eur * pct / 100.0, 2)
        assert fee["transfer_type"] == ttype
        assert fee["amount_eur"] == amount_eur
        assert fee["flat_fee_eur"] == flat
        assert fee["percent_fee"] == pct
        assert fee["total_fee_eur"] == expected_total


def test_transfer_fee_invalid_type():
    with pytest.raises(ValueError, match="Unknown transfer type: invalid"):
        fx.transfer_fee(100.0, "invalid")

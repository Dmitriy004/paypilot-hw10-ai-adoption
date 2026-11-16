# tests/generated/test_fx_generated.py
import pytest

from app.engines import fx
from app.engines import policy


def test_mid_rate_known_currencies():
    # Use known currencies from policy.RATES_TO_EUR
    for from_cur in policy.RATES_TO_EUR:
        for to_cur in policy.RATES_TO_EUR:
            rate = fx.mid_rate(from_cur, to_cur)
            expected = policy.RATES_TO_EUR[from_cur] / policy.RATES_TO_EUR[to_cur]
            assert rate == expected


def test_mid_rate_unknown_currency_raises():
    with pytest.raises(ValueError, match="Unknown currency"):
        fx.mid_rate("XXX", "EUR")
    with pytest.raises(ValueError, match="Unknown currency"):
        fx.mid_rate("EUR", "YYY")


def test_quote_unknown_tier_raises():
    with pytest.raises(ValueError, match="Unknown tier"):
        fx.quote(100, "EUR", "USD", "unknown_tier")


def test_quote_within_allowance_no_spread():
    tier = next(iter(policy.TIERS))
    amount = 10.0
    from_cur = next(iter(policy.RATES_TO_EUR))
    to_cur = from_cur
    allowance = policy.FX_FREE_MONTHLY_ALLOWANCE_EUR[tier]
    # Use amount such that allowance_used + amount_eur <= allowance_total
    amount_eur = policy.to_eur(amount, from_cur)
    allowance_used = allowance - amount_eur
    q = fx.quote(amount, from_cur, to_cur, tier, allowance_used_eur=allowance_used)
    assert q.allowance_applied is True
    assert q.spread_pct == 0.0
    assert q.final_amount == pytest.approx(q.gross_amount)


def test_quote_exceed_allowance_default_spread():
    tier = next(iter(policy.TIERS))
    amount = 1000.0
    from_cur = next(iter(policy.RATES_TO_EUR))
    to_cur = from_cur
    allowance = policy.FX_FREE_MONTHLY_ALLOWANCE_EUR[tier]
    allowance_used = 0.0
    q = fx.quote(amount, from_cur, to_cur, tier, allowance_used_eur=allowance_used)
    assert q.allowance_applied is False
    assert q.spread_pct == policy.FX_SPREAD_PCT[tier]
    assert q.spread_amount == pytest.approx(q.gross_amount * q.spread_pct / 100)


def test_quote_exceed_allowance_spread_override():
    tier = next(iter(policy.TIERS))
    amount = 1000.0
    from_cur = next(iter(policy.RATES_TO_EUR))
    to_cur = from_cur
    allowance_used = 0.0
    override = 5.0
    q = fx.quote(amount, from_cur, to_cur, tier,
                 allowance_used_eur=allowance_used,
                 spread_pct_override=override)
    assert q.spread_pct == override
    assert q.spread_amount == pytest.approx(q.gross_amount * override / 100)


def test_quote_partial_allowance_applied():
    tier = next(iter(policy.TIERS))
    from_cur = next(iter(policy.RATES_TO_EUR))
    to_cur = from_cur
    allowance = policy.FX_FREE_MONTHLY_ALLOWANCE_EUR[tier]
    amount = 1000.0
    # Set allowance_used_eur so partial allowance applies
    allowance_used = allowance * 0.8
    q = fx.quote(amount, from_cur, to_cur, tier,
                 allowance_used_eur=allowance_used,
                 partial_allowance=True)
    amount_eur = policy.to_eur(amount, from_cur)
    remaining_eur = max(0.0, allowance - allowance_used)
    charged_eur = max(0.0, amount_eur - remaining_eur)
    charged_share = charged_eur / amount_eur if amount_eur else 0.0
    expected_spread = q.gross_amount * charged_share * q.spread_pct / 100.0
    assert q.spread_amount == pytest.approx(expected_spread)


def test_quote_as_dict_rounds_floats():
    tier = next(iter(policy.TIERS))
    from_cur = next(iter(policy.RATES_TO_EUR))
    to_cur = from_cur
    q = fx.quote(100.123456789, from_cur, to_cur, tier)
    d = q.as_dict()
    for k, v in d.items():
        if isinstance(v, float):
            # 6 decimal places
            assert round(v, 6) == v


def test_transfer_fee_known_types():
    for ttype, (flat, pct) in policy.TRANSFER_FEES.items():
        amount_eur = 100.0
        result = fx.transfer_fee(amount_eur, ttype)
        expected_fee = flat + amount_eur * pct / 100.0
        assert result["transfer_type"] == ttype
        assert result["amount_eur"] == amount_eur
        assert result["flat_fee_eur"] == flat
        assert result["percent_fee"] == pct
        assert result["total_fee_eur"] == round(expected_fee, 2)


def test_transfer_fee_unknown_type_raises():
    with pytest.raises(ValueError, match="Unknown transfer type"):
        fx.transfer_fee(100.0, "unknown_type")

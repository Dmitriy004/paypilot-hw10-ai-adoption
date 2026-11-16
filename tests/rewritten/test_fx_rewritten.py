import pytest

from app.engines import fx


@pytest.mark.parametrize(
    ("from_currency", "to_currency", "expected_rate"),
    [
        ("EUR", "USD", 1.0869565217391304),
        ("USD", "EUR", 0.92),
        ("GBP", "PLN", 5.086956521739131),
        ("CHF", "CHF", 1.0),
    ],
)
def test_mid_rate_known_currencies_rewritten(from_currency, to_currency, expected_rate):
    """HR-G01: assert independently specified rates, not a copied implementation formula."""
    assert fx.mid_rate(from_currency, to_currency) == pytest.approx(expected_rate)


def test_quote_partial_allowance_applied_rewritten():
    """HR-G07: tier1 has EUR 500 free, EUR 400 used, EUR 100 still free."""
    quote = fx.quote(
        amount=1000.0,
        from_currency="EUR",
        to_currency="EUR",
        tier="tier1",
        allowance_used_eur=400.0,
        partial_allowance=True,
    )

    # 900 EUR charged at 1.5%, while 100 EUR remains free.
    assert quote.allowance_total_eur == 500.0
    assert quote.allowance_used_before_eur == 400.0
    assert quote.allowance_applied is False
    assert quote.mid_rate == pytest.approx(1.0)
    assert quote.spread_pct == pytest.approx(1.5)
    assert quote.gross_amount == pytest.approx(1000.0)
    assert quote.spread_amount == pytest.approx(13.5)
    assert quote.final_amount == pytest.approx(986.5)


def test_quote_as_dict_rounds_floats_rewritten():
    """HR-G08: compare complete serialized output with fixed six-decimal values."""
    quote = fx.quote(
        amount=100.123456789,
        from_currency="USD",
        to_currency="EUR",
        tier="tier1",
    )

    assert quote.as_dict() == {
        "from_currency": "USD",
        "to_currency": "EUR",
        "amount": 100.123457,
        "mid_rate": 0.92,
        "tier": "tier1",
        "spread_pct": 0.0,
        "allowance_total_eur": 500,
        "allowance_used_before_eur": 0.0,
        "allowance_applied": True,
        "gross_amount": 92.11358,
        "spread_amount": 0.0,
        "final_amount": 92.11358,
    }

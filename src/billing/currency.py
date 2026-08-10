"""Decimal rules for the currencies invoices are rendered in."""

from decimal import ROUND_HALF_UP, Decimal

#: Currencies with no minor unit: amounts are whole units, written undecimalised.
ZERO_DECIMAL_CURRENCIES = frozenset({"JPY", "KRW", "VND"})

DEFAULT_DECIMAL_PLACES = 2


def decimal_places(currency: str) -> int:
    """Return the number of decimal places ``currency`` is written with."""

    if currency.upper() in ZERO_DECIMAL_CURRENCIES:
        return 0
    return DEFAULT_DECIMAL_PLACES


def round_amount(amount: float, currency: str) -> float:
    """Round ``amount`` to the smallest unit of ``currency``.

    Half-way amounts round up, the convention an invoice is expected to follow;
    the built-in ``round`` would settle 1234.5 JPY down to 1234.
    """

    quantum = Decimal(1).scaleb(-decimal_places(currency))
    return float(Decimal(str(amount)).quantize(quantum, rounding=ROUND_HALF_UP))


def format_amount(amount: float, currency: str) -> str:
    """Render ``amount`` with the decimal places ``currency`` is written with."""

    places = decimal_places(currency)
    return f"{round_amount(amount, currency):.{places}f}"

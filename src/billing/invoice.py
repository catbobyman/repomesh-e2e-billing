"""Invoice rendering for settled checkout orders."""

from pricing_core import quote


def render_invoice(
    items,
    shipping: float = 0.0,
    discount_rate: float = 0.0,
    tax_rate: float = 0.0,
    currency: str = "USD",
    credit_note: float = 0.0,
) -> dict:
    """Return the invoice the customer receives."""

    priced = quote(
        items,
        shipping=shipping,
        discount_rate=discount_rate,
        tax_rate=tax_rate,
    )
    due = max(round(priced.amount - credit_note, 2), 0.0)
    return {
        "amount_due": due,
        "currency": "USD",
        "line_count": len(items),
    }

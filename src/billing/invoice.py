"""Invoice rendering for settled checkout orders."""

from pricing_core import quote

from .currency import format_amount, round_amount


def render_invoice(
    items,
    shipping: float = 0.0,
    discount_rate: float = 0.0,
    tax_rate: float = 0.0,
    currency: str = "USD",
    credit_note: float = 0.0,
) -> dict:
    """Return the invoice the customer receives, priced in ``currency``.

    Every monetary amount is rounded to the smallest unit of ``currency``, so a
    zero-decimal currency such as JPY yields whole amounts throughout.
    """

    priced = quote(
        items,
        shipping=shipping,
        discount_rate=discount_rate,
        tax_rate=tax_rate,
        currency=currency,
    )
    invoice_currency = priced.currency
    total = round_amount(priced.amount, invoice_currency)
    credit = round_amount(credit_note, invoice_currency)
    due = max(round_amount(total - credit, invoice_currency), 0.0)
    return {
        "amount_due": due,
        "amount_due_display": format_amount(due, invoice_currency),
        "total": total,
        "total_display": format_amount(total, invoice_currency),
        "credit_note": credit,
        "credit_note_display": format_amount(credit, invoice_currency),
        "currency": invoice_currency,
        "line_count": len(items),
        "lines": [
            {
                "name": item.name,
                "quantity": item.quantity,
                "amount": round_amount(item.amount, invoice_currency),
                "amount_display": format_amount(item.amount, invoice_currency),
            }
            for item in items
        ],
    }

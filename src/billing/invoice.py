"""Invoice rendering for settled checkout orders."""

from collections.abc import Mapping

from pricing_core import quote

UNSPECIFIED_PAYMENT_METHOD = "Unspecified"


def _payment_method(order) -> str:
    """Read the payment method off the order backing this invoice."""

    if order is None:
        return UNSPECIFIED_PAYMENT_METHOD
    if isinstance(order, Mapping):
        method = order.get("payment_method")
    else:
        method = getattr(order, "payment_method", None)
    return method or UNSPECIFIED_PAYMENT_METHOD


def _detail_lines(items, amount_due: float, currency: str, order) -> list[str]:
    """Render the invoice body, payment method last."""

    lines = [
        f"{item.name} x{item.quantity}: {item.amount:.2f} {currency}" for item in items
    ]
    lines.append(f"Amount Due: {amount_due:.2f} {currency}")
    lines.append(f"Payment Method: {_payment_method(order)}")
    return lines


def render_invoice(
    items,
    shipping: float = 0.0,
    discount_rate: float = 0.0,
    tax_rate: float = 0.0,
    currency: str = "USD",
    credit_note: float = 0.0,
    order=None,
) -> dict:
    """Return the invoice the customer receives."""

    priced = quote(
        items,
        shipping=shipping,
        discount_rate=discount_rate,
        tax_rate=tax_rate,
        currency=currency,
    )
    due = max(round(priced.amount - credit_note, 2), 0.0)
    return {
        "amount_due": due,
        "currency": priced.currency,
        "line_count": len(items),
        "details": _detail_lines(items, due, priced.currency, order),
    }

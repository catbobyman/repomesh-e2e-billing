"""Frozen quoting contract — the interface this repository codes against.

This is a materialisation of the agreed contract, not the producer's release.
Unit tests run against it so the consumer can be developed and verified before
repomesh-e2e-pricing-core ships the implementation. Joint tests replace it with
the real producer at its candidate revision (see scripts/run_tests.py).

Do not edit to work around a failing test: changing this file changes the
contract, which is a cross-repository decision.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class LineItem:
    name: str
    unit_price: float
    quantity: int

    @property
    def amount(self) -> float:
        return self.unit_price * self.quantity


@dataclass(frozen=True)
class Quote:
    amount: float
    currency: str


def quote(
    items: list[LineItem],
    shipping: float = 0.0,
    discount_rate: float = 0.0,
    tax_rate: float = 0.0,
    currency: str = "USD",
) -> Quote:
    merchandise = sum(item.amount for item in items)
    payable = merchandise * (1 - discount_rate) + shipping
    payable = payable * (1 + tax_rate)
    return Quote(amount=round(payable, 2), currency=currency)

import unittest

from billing.invoice import render_invoice
from pricing_core import LineItem


class InvoiceAmountTests(unittest.TestCase):
    def test_invoice_reports_the_payable_amount(self) -> None:
        invoice = render_invoice([LineItem("book", 10.0, 2)], shipping=5.0)
        self.assertEqual(invoice["amount_due"], 25.0)

    def test_credit_note_never_pushes_the_invoice_below_zero(self) -> None:
        invoice = render_invoice([LineItem("book", 10.0, 1)], credit_note=40.0)
        self.assertEqual(invoice["amount_due"], 0.0)


class InvoiceCurrencyTests(unittest.TestCase):
    """Multi-currency support, verified against the frozen contract."""

    def test_invoice_reports_the_requested_currency(self) -> None:
        invoice = render_invoice([LineItem("book", 10.0, 1)], currency="EUR")
        self.assertEqual(invoice["currency"], "EUR")

    def test_invoice_defaults_to_usd(self) -> None:
        invoice = render_invoice([LineItem("book", 10.0, 1)])
        self.assertEqual(invoice["currency"], "USD")


if __name__ == "__main__":
    unittest.main()

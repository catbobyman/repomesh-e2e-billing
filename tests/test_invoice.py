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

    def test_line_items_carry_the_invoice_currency_amounts(self) -> None:
        invoice = render_invoice(
            [LineItem("book", 10.0, 2), LineItem("pen", 1.5, 1)], currency="EUR"
        )
        self.assertEqual(
            [line["amount_display"] for line in invoice["lines"]], ["20.00", "1.50"]
        )


class ZeroDecimalCurrencyTests(unittest.TestCase):
    """JPY, KRW and VND have no minor unit: whole amounts, no decimal point."""

    def test_amount_due_is_rounded_to_a_whole_unit(self) -> None:
        invoice = render_invoice([LineItem("book", 999.5, 1)], currency="JPY")
        self.assertEqual(invoice["amount_due"], 1000.0)
        self.assertEqual(invoice["amount_due_display"], "1000")

    def test_line_items_are_rounded_to_whole_units(self) -> None:
        invoice = render_invoice(
            [LineItem("book", 1200.4, 1), LineItem("pen", 99.5, 3)], currency="KRW"
        )
        self.assertEqual(
            [line["amount_display"] for line in invoice["lines"]], ["1200", "299"]
        )

    def test_credit_note_is_rounded_to_a_whole_unit(self) -> None:
        invoice = render_invoice(
            [LineItem("book", 1000.0, 1)], currency="VND", credit_note=250.6
        )
        self.assertEqual(invoice["credit_note_display"], "251")
        self.assertEqual(invoice["amount_due_display"], "749")

    def test_decimal_currencies_keep_their_minor_unit(self) -> None:
        invoice = render_invoice([LineItem("book", 999.5, 1)], currency="USD")
        self.assertEqual(invoice["amount_due"], 999.5)
        self.assertEqual(invoice["amount_due_display"], "999.50")


if __name__ == "__main__":
    unittest.main()

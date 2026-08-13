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
        for requested in ("EUR", "JPY", "GBP"):
            with self.subTest(currency=requested):
                invoice = render_invoice(
                    [LineItem("book", 10.0, 1)], currency=requested
                )
                self.assertEqual(invoice["currency"], requested)

    def test_invoice_defaults_to_usd(self) -> None:
        invoice = render_invoice([LineItem("book", 10.0, 1)])
        self.assertEqual(invoice["currency"], "USD")


class InvoicePaymentMethodTests(unittest.TestCase):
    def test_payment_method_is_the_last_detail_line(self) -> None:
        invoice = render_invoice(
            [LineItem("book", 10.0, 1)], order={"payment_method": "Credit Card"}
        )
        self.assertEqual(invoice["details"][-1], "Payment Method: Credit Card")

    def test_payment_method_comes_from_the_order(self) -> None:
        invoice = render_invoice(
            [LineItem("book", 10.0, 1)],
            order={"payment_method": "Cash on Delivery"},
        )
        self.assertEqual(invoice["details"][-1], "Payment Method: Cash on Delivery")

    def test_invoice_without_an_order_reports_an_unspecified_method(self) -> None:
        invoice = render_invoice([LineItem("book", 10.0, 1)])
        self.assertEqual(invoice["details"][-1], "Payment Method: Unspecified")


if __name__ == "__main__":
    unittest.main()

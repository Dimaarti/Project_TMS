from decimal import Decimal
from unittest import TestCase

from china_calc.client.forms import ClientForm


class TestClientForm(TestCase):
    def valid_data(self, **kwargs):
        data = {
            "full_name": "Иваненко Иван",
            "phone": "+375290000000",
            "address": "г. Минск, ул. Пушкина д.0",
            "buyer_commission_percent": "10.00",
        }

        data.update(kwargs)
        return data

    def test_accepts_valid_data(self):
        form = ClientForm(data=self.valid_data())

        self.assertTrue(form.is_valid(), form.errors)
        self.assertEqual(form.cleaned_data["full_name"], "Иваненко Иван")

        self.assertEqual(form.cleaned_data["buyer_commission_percent"], Decimal("10.00"))

    def test_address_is_optional(self):
        form = ClientForm(data=self.valid_data(address=""))

        self.assertTrue(form.is_valid(), form.errors)

    def test_commission_rejects_value_outside_range(self):
        for value in ("-0.01", "100.01"):
            with self.subTest(value=value):
                form = ClientForm(data=self.valid_data(buyer_commission_percent=value))

                self.assertFalse(form.is_valid())
                self.assertIn("buyer_commission_percent", form.errors)

    def test_form_contains_only_editable_fields_in_expected_order(self):
        form = ClientForm()

        self.assertEqual(
            list(form.fields),
            [
                "full_name",
                "phone",
                "address",
                "buyer_commission_percent",
            ],
        )

        self.assertNotIn("user", form.fields)

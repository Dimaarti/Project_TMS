import datetime
from decimal import Decimal

from django.test import TestCase

from china_calc.finance.forms import ExchangeRateForm, ShipmentCalculateForm
from china_calc.finance.models.exchange_rate import ExchangeRate


class TestExchangeRateForm(TestCase):
    def setUp(self):
        self.data = {
            "date": datetime.date.today(),
            "cny_to_byn": 0.4500,
            "cny_to_byn_client": 0.5000,
            "cny_to_rub": 12.0000,
            "cny_to_rub_client": 13.0000,
            "usd_to_byn": 3.2000,
            "usd_to_byn_client": 3.3000,
            "usd_to_rub": 90.0000,
            "usd_to_rub_client": 92.0000,
            "rub_to_byn": 0.0350,
            "rub_to_byn_client": 0.0500,
        }

    def test_valid_form(self):
        form = ExchangeRateForm(data=self.data)
        self.assertTrue(form.is_valid())

    def test_date_is_required(self):
        data = self.data.copy()
        data["date"] = ""
        form = ExchangeRateForm(data=data)

        self.assertFalse(form.is_valid())

    def test_rate_be_number(self):
        data = self.data.copy()
        data["cny_to_byn"] = "текст"
        form = ExchangeRateForm(data=data)

        self.assertFalse(form.is_valid())

    def test_rate_is_converted_to_decimal(self):
        form = ExchangeRateForm(data=self.data)

        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["cny_to_byn"], Decimal("0.4500"))


class TestShipmentCalculateForm(TestCase):
    def setUp(self):
        self.exchange_rate = ExchangeRate.objects.create(
            date=datetime.date.today(),
            cny_to_byn=0.4500,
            cny_to_byn_client=0.5000,
            cny_to_rub=12.0000,
            cny_to_rub_client=13.0000,
            usd_to_byn=3.2000,
            usd_to_byn_client=3.3000,
            usd_to_rub=90.0000,
            usd_to_rub_client=92.0000,
            rub_to_byn=0.0350,
            rub_to_byn_client=0.0500,
        )

        self.data = {
            "exchange_rate": self.exchange_rate.pk,
            "base_currency": "CNY",
            "counter_currency": "BYN",
            "purchase_cost": 2000.00,
            "client_purchase_cost": 3000.00,
            "logistics_cost": 4000.00,
            "buyer_commission_cost": 5000.00,
            "price_cost": 10000.00,
            "client_price_cost": 10000.00,
            "profit_cost": 20000.00,
            "additional_services": 50.00,
        }

    def test_form_is_valid(self):
        form = ShipmentCalculateForm(data=self.data)

        self.assertTrue(form.is_valid())

    def test_exchange_rate_is_required(self):
        data = self.data.copy()
        data["exchange_rate"] = ""
        form = ShipmentCalculateForm(data=data)

        self.assertFalse(form.is_valid())

    def cost_must_be_number(self):
        data = self.data.copy()
        data[
            "purchase_cost",
            "client_purchase_cost",
            "logistics_cost",
            "buyer_commission_cost",
            "price_cost",
            "client_price_cost",
            "profit_cost",
            "additional_services",
        ] = "не число"
        form = ShipmentCalculateForm(data=data)

        self.assertFalse(form.is_valid())

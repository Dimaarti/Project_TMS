import datetime

from django.test import Client, TestCase

from china_calc.account.models import User
from china_calc.finance.models.exchange_rate import ExchangeRate
from china_calc.logistics.models import Route
from china_calc.shipment.models import Shipment
from config.model_choices import (
    Currency,
    LogisticCalculationMethod,
    SettlementFinalCurrency,
)


class TestShipmentForm(TestCase):
    def setUp(self):
        self.client = Client()
        test_user_email = "test@test.com"
        test_user_password = "1111"
        self.user = User.objects.create_user(
            email=test_user_email, password=test_user_password
        )
        self.client.force_login(self.user)

    def test_shipment_create(self):
        path = "/shipment/create/"
        test_shipment_number = "test shipment number"
        test_route = Route.objects.create(name="test route")
        test_exchange_rate = ExchangeRate.objects.create(
            date=datetime.date.today(),
            cny_to_byn=3,
            cny_to_byn_client=3,
            cny_to_rub=3,
            cny_to_rub_client=3,
            usd_to_byn=3,
            usd_to_byn_client=3,
            usd_to_rub=3,
            usd_to_rub_client=3,
            rub_to_byn=3,
            rub_to_byn_client=3,
        )
        test_tariff_one_kg = 3
        test_tariff_currency = Currency.USD
        test_settlement_final_currency = SettlementFinalCurrency.BYN
        test_status = "test status"
        test_weight = 10
        test_volume = 15
        test_logistic_calculation_type = LogisticCalculationMethod.WEIGHT
        test_tariff_one_m3 = 15
        test_note = "test note"

        body = {
            "number": test_shipment_number,
            "route": test_route.pk,
            "exchange_rate": test_exchange_rate.pk,
            "tariff_one_kg": test_tariff_one_kg,
            "tariff_currency": test_tariff_currency,
            "settlement_final_currency": test_settlement_final_currency,
            "status": test_status,
            "weight": test_weight,
            "volume": test_volume,
            "logistic_calculation_type": test_logistic_calculation_type,
            "tariff_one_m3": test_tariff_one_m3,
            "note": test_note,
        }

        response = self.client.post(path=path, data=body)
        self.assertEqual(response.status_code, 302)

        shipment = Shipment.objects.all()

        self.assertEqual(len(shipment), 1)
        self.assertEqual(shipment[0].number, test_shipment_number)
        self.assertEqual(shipment[0].route, test_route)
        self.assertEqual(shipment[0].exchange_rate, test_exchange_rate)
        self.assertEqual(shipment[0].tariff_one_kg, test_tariff_one_kg)
        self.assertEqual(shipment[0].tariff_currency, test_tariff_currency)
        self.assertEqual(
            shipment[0].settlement_final_currency, test_settlement_final_currency
        )
        self.assertEqual(shipment[0].status, test_status)
        self.assertEqual(shipment[0].weight, test_weight)
        self.assertEqual(shipment[0].volume, test_volume)
        self.assertEqual(
            shipment[0].logistic_calculation_type, test_logistic_calculation_type
        )
        self.assertEqual(shipment[0].tariff_one_m3, test_tariff_one_m3)
        self.assertEqual(shipment[0].note, test_note)

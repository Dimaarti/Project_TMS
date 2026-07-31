import datetime

from django.test import Client, TestCase
from django.urls import reverse

from china_calc.account.models import User
from china_calc.finance.models.exchange_rate import ExchangeRate
from china_calc.logistics.models import Route
from china_calc.shipment.models import Shipment
from config.model_choices import (
    Currency,
    LogisticCalculationMethod,
    SettlementFinalCurrency,
)


class TestShipmentView(TestCase):
    def setUp(self):
        self.client = Client()
        test_user_email = "test@test.com"
        test_user_password = "1111"
        self.user = User.objects.create_user(
            email=test_user_email, password=test_user_password
        )
        self.client.force_login(self.user)

        self.test_shipment_number = "test shipment"

        self.test_route = Route.objects.create(
            name="test route",
        )

        self.test_exchange_rate = ExchangeRate.objects.create(
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

        self.test_tariff_one_kg = 3
        self.test_tariff_currency = Currency.USD
        self.test_settlement_final_currency = SettlementFinalCurrency.BYN
        self.test_status = "test status"
        self.test_weight = 10
        self.test_volume = 15
        self.test_logistic_calculation_type = LogisticCalculationMethod.WEIGHT
        self.test_tariff_one_m3 = 15
        self.test_note = "test note"

        self.shipment = Shipment.objects.create(
            user=self.user,
            number="test_shipment_number",
            route=self.test_route,
            exchange_rate=self.test_exchange_rate,
            tariff_one_kg=2,
            tariff_currency=Currency.USD,
            settlement_final_currency=Currency.BYN,
            status="test_status",
            weight=20,
            volume=20,
            logistic_calculation_type=LogisticCalculationMethod.WEIGHT,
            tariff_one_m3=30,
            note="test_note",
        )

    def test_shipment_list(self):
        response = self.client.get(reverse("shipment:list"))
        shipment = response.context["shipment"]

        self.assertEqual(response.status_code, 200)

        self.assertEqual(len(shipment), 1)
        self.assertEqual(shipment[0], self.shipment)
        self.assertTemplateUsed(response, "shipment/shipment_list.html")

    def test_shipment_detail(self):
        response = self.client.get(
            reverse("shipment:detail", kwargs={"pk": self.shipment.pk})
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["shipment"], self.shipment)

    def test_shipment_update(self):
        data = {
            "number": "test_shipment_number",
            "route": self.test_route.pk,
            "exchange_rate": self.test_exchange_rate.pk,
            "tariff_one_kg": 2,
            "tariff_currency": Currency.USD,
            "settlement_final_currency": Currency.BYN,
            "status": "test_status",
            "weight": 20,
            "volume": 20,
            "logistic_calculation_type": LogisticCalculationMethod.WEIGHT,
            "tariff_one_m3": 30,
            "note": "test_note"
        }
        response = self.client.post(
            reverse("shipment:update", kwargs={"pk": self.shipment.pk}),
            data=data,
        )

        self.assertEqual(response.status_code, 302)
        self.shipment.refresh_from_db()
        self.assertEqual(self.shipment.number, "test_shipment_number")
        self.assertEqual(self.shipment.route, self.test_route)
        self.assertEqual(self.shipment.exchange_rate, self.test_exchange_rate)
        self.assertEqual(self.shipment.tariff_one_kg, 2)
        self.assertEqual(self.shipment.tariff_currency, Currency.USD)
        self.assertEqual(self.shipment.settlement_final_currency, Currency.BYN)
        self.assertEqual(self.shipment.status, "test_status")
        self.assertEqual(self.shipment.weight, 20)
        self.assertEqual(self.shipment.volume, 20)
        self.assertEqual(self.shipment.logistic_calculation_type, LogisticCalculationMethod.WEIGHT)
        self.assertEqual(self.shipment.tariff_one_m3, 30)
        self.assertEqual(self.shipment.note, "test_note")

    def test_shipment_delete(self):
        response = self.client.post(
            reverse("shipment:delete", kwargs={"pk": self.shipment.pk})
        )

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("shipment:list"))

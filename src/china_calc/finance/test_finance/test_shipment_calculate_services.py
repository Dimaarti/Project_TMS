import datetime
from decimal import Decimal

from django.test import TestCase

from china_calc.account.models import User
from china_calc.client.models import Client
from china_calc.finance.models.exchange_rate import ExchangeRate
from china_calc.finance.services.shipment_calculate_service import (
    ShipmentCalculatorService,
)
from china_calc.logistics.models import Route
from china_calc.shipment.models import Shipment, ShipmentExpense, ShipmentItem
from config.model_choices import (
    Currency,
    ExpenseType,
    LogisticCalculationMethod,
    TransportType,
)


class TestShipmentCalculatorService(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="test@test.com",
            password="test",
        )

        self.route = Route.objects.create(
            dispatch_country="Китай",
            destination_country="Беларусь",
            transport_type=TransportType.AUTO,
        )

        self.exchange_rate = ExchangeRate.objects.create(
            user=self.user,
            date=datetime.date.today(),
            cny_to_byn=Decimal(1),
            cny_to_byn_client=Decimal(2),
            cny_to_rub=Decimal(1),
            cny_to_rub_client=Decimal(2),
            usd_to_byn=Decimal(1),
            usd_to_byn_client=Decimal(2),
            usd_to_rub=Decimal(1),
            usd_to_rub_client=Decimal(2),
            rub_to_byn=Decimal(1),
            rub_to_byn_client=Decimal(2),
        )

        self.shipment = Shipment.objects.create(
            user=self.user,
            number="Test 1",
            route=self.route,
            exchange_rate=self.exchange_rate,
            logistic_calculation_type=LogisticCalculationMethod.WEIGHT,
            weight=Decimal(50),
            volume=Decimal(0),
            tariff_one_kg=Decimal("3.5"),
            tariff_one_m3=Decimal(0),
            tariff_currency=Currency.USD,
            settlement_final_currency=Currency.BYN,
        )

        self.first_client = Client.objects.create(
            user=self.user,
            full_name="Клиент 1",
            phone="22",
            buyer_commission_percent=Decimal(5),
        )
        self.second_client = Client.objects.create(
            user=self.user,
            full_name="Клиент 2",
            phone="22",
            buyer_commission_percent=Decimal(10),
        )

        self.first_item = ShipmentItem.objects.create(
            shipment=self.shipment,
            client=self.first_client,
            name="Товар 1",
            quantity=1,
            price=Decimal(150),
            price_currency=Currency.CNY,
            weight=Decimal(5),
            volume=Decimal(0),
        )
        self.second_item = ShipmentItem.objects.create(
            shipment=self.shipment,
            client=self.second_client,
            name="Товар 2",
            quantity=2,
            price=Decimal(100),
            price_currency=Currency.CNY,
            weight=Decimal(10),
            volume=Decimal(0),
        )

        ShipmentExpense.objects.create(
            shipment=self.shipment,
            expense_type=ExpenseType.INSURANCE,
            amount=Decimal(5),
            currency=Currency.USD,
        )
        ShipmentExpense.objects.create(
            shipment=self.shipment,
            item=self.first_item,
            expense_type=ExpenseType.ITEM_PACKAGING,
            amount=Decimal(3),
            currency=Currency.USD,
        )

    # проверка получения общего результата поставки
    def test_calculate_shipment_result(self):
        result = ShipmentCalculatorService.calculate(shipment=self.shipment)

        self.assertEqual(result.purchase_cost, Decimal(350))
        self.assertEqual(result.client_purchase_cost, Decimal(700))
        self.assertEqual(result.logistics_cost, Decimal(175))
        self.assertEqual(result.expenses_cost, Decimal(8))
        self.assertEqual(result.buyer_commission_cost, Decimal(55))
        self.assertEqual(result.price_cost, Decimal(533))
        self.assertEqual(result.client_price_cost, Decimal(938))
        self.assertEqual(result.profit_cost, Decimal(405))

    # проверка созданных результатов клиентов
    def test_creates_client_results(self):
        result = ShipmentCalculatorService.calculate(shipment=self.shipment)

        self.assertEqual(result.client_results.count(), 2)

        first_result = result.client_results.get(client=self.first_client)

        self.assertEqual(first_result.purchase_cost, Decimal(150))
        self.assertEqual(first_result.client_purchase_cost, Decimal(300))
        self.assertEqual(first_result.logistics_cost, Decimal("58.33"))
        self.assertEqual(first_result.expenses_cost, Decimal("4.67"))
        self.assertEqual(first_result.buyer_commission_cost, Decimal(15))
        self.assertEqual(first_result.price_cost, Decimal(213))
        self.assertEqual(first_result.client_price_cost, Decimal(378))
        self.assertEqual(first_result.profit_cost, Decimal(165))

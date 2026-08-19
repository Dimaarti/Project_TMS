from decimal import Decimal
from types import SimpleNamespace
from unittest import TestCase

from china_calc.finance.calculators.currency_calculator import CurrencyCalculator
from config.model_choices import Currency


class TestCurrencyConverter(TestCase):
    def setUp(self):
        self.exchange_rate = SimpleNamespace(
            cny_to_byn=Decimal("0.45"),
            cny_to_byn_client=Decimal("0.50"),
            cny_to_rub=Decimal(13),
            cny_to_rub_client=Decimal(14),
            usd_to_byn=Decimal("2.90"),
            usd_to_byn_client=Decimal("3.10"),
            usd_to_rub=Decimal(89),
            usd_to_rub_client=Decimal(93),
            rub_to_byn=Decimal("3.6327"),
            rub_to_byn_client=Decimal("3.7000"),
        )

    # проверка курса себестоимости
    def test_converts_cny_to_byn(self):
        result = CurrencyCalculator.convert_currency(
            amount=Decimal(100),
            purchase_currency=Currency.CNY,
            final_currency=Currency.BYN,
            exchange_rate=self.exchange_rate,
        )

        self.assertEqual(result, Decimal("45.00"))

    # проверка клиентского курса
    def test_converts_cny_to_byn_client(self):
        result = CurrencyCalculator.convert_currency(
            amount=Decimal(100),
            purchase_currency=Currency.CNY,
            final_currency=Currency.BYN,
            exchange_rate=self.exchange_rate,
            for_client=True,
        )

        self.assertEqual(result, Decimal("50.00"))

    # проверка, если валюты одинаковые
    def test_converts_byn_to_byn(self):
        result = CurrencyCalculator.convert_currency(
            amount=Decimal(100),
            purchase_currency=Currency.BYN,
            final_currency=Currency.BYN,
            exchange_rate=self.exchange_rate,
        )

        self.assertEqual(result, Decimal("100.00"))

    # проверка нулевой суммы
    def test_converts_zero_amount(self):
        result = CurrencyCalculator.convert_currency(
            amount=Decimal(0),
            purchase_currency=Currency.CNY,
            final_currency=Currency.BYN,
            exchange_rate=self.exchange_rate,
        )

        self.assertEqual(result, Decimal(0))

    # проверка отрицательной суммы
    def test_rejects_negative_amount(self):
        with self.assertRaisesRegex(ValueError, "Сумма не может быть отрицательной"):
            CurrencyCalculator.convert_currency(
                amount=Decimal(-1),
                purchase_currency=Currency.CNY,
                final_currency=Currency.BYN,
                exchange_rate=self.exchange_rate,
            )

    # проверка неподдерживаемого направления
    def test_unsupported_exchange_rate(self):
        with self.assertRaises(
            ValueError,
        ):
            CurrencyCalculator.convert_currency(
                amount=Decimal(100),
                purchase_currency=Currency.BYN,
                final_currency=Currency.CNY,
                exchange_rate=self.exchange_rate,
            )

    # проверка при отсутствующем поле курса
    def test_missing_rate_field(self):
        exchange_rate = SimpleNamespace()

        with self.assertRaisesRegex(
            ValueError, "В модели обменного курса отсутствует поле - cny_to_byn"
        ):
            CurrencyCalculator.convert_currency(
                amount=Decimal(100),
                purchase_currency=Currency.CNY,
                final_currency=Currency.BYN,
                exchange_rate=exchange_rate,
            )

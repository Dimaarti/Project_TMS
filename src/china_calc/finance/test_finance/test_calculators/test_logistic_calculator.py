from decimal import Decimal
from types import SimpleNamespace
from unittest import TestCase

from china_calc.finance.calculators.logistic_calculator import LogisticCalculator
from config.model_choices import Currency, LogisticCalculationMethod


class TestLogisticCalculator(TestCase):
    # проверка расчета по весу
    def test_calculate_logistic_by_weight(self):
        shipment = SimpleNamespace(
            logistic_calculation_type=LogisticCalculationMethod.WEIGHT,
            weight=Decimal(25),
            volume=Decimal(0),
            tariff_one_kg=Decimal("3.5"),
            tariff_one_m3=Decimal(0),
            tariff_currency=Currency.USD,
            settlement_final_currency=Currency.BYN,
            exchange_rate=SimpleNamespace(
                usd_to_byn=Decimal("2.90"),
            ),
        )

        result = LogisticCalculator.calculate(
            shipment=shipment,
        )

        self.assertEqual(result, Decimal("253.75"))

    # проверка расчета по объему
    def test_calculate_logistic_by_volume(self):
        shipment = SimpleNamespace(
            logistic_calculation_type=LogisticCalculationMethod.VOLUME,
            weight=Decimal(0),
            volume=Decimal("0.035"),
            tariff_one_kg=Decimal(0),
            tariff_one_m3=Decimal(350),
            tariff_currency=Currency.USD,
            settlement_final_currency=Currency.BYN,
            exchange_rate=SimpleNamespace(
                usd_to_byn=Decimal("2.90"),
            ),
        )

        result = LogisticCalculator.calculate(
            shipment=shipment,
        )

        self.assertEqual(result, Decimal("35.525"))

    # проверка нулевого веса поставки
    def test_zero_weight(self):
        shipment = SimpleNamespace(
            logistic_calculation_type=LogisticCalculationMethod.WEIGHT,
            weight=Decimal(0),
            tariff_one_kg=Decimal("3.5"),
        )

        with self.assertRaisesRegex(ValueError, "Вес поставки должен быть больше 0"):
            LogisticCalculator.calculate(
                shipment=shipment,
            )

    # проверка нулевого объема поставки
    def test_zero_volume(self):
        shipment = SimpleNamespace(
            logistic_calculation_type=LogisticCalculationMethod.VOLUME,
            volume=Decimal(0),
            tariff_one_m3=Decimal(350),
        )

        with self.assertRaisesRegex(ValueError, "Объем поставки должен быть больше 0"):
            LogisticCalculator.calculate(
                shipment=shipment,
            )

    # проверка нулевой стоимости тарифа веса
    def test_zero_tariff_one_kg(self):
        shipment = SimpleNamespace(
            logistic_calculation_type=LogisticCalculationMethod.WEIGHT,
            weight=Decimal(20),
            tariff_one_kg=Decimal(0),
        )

        with self.assertRaisesRegex(ValueError, "Тариф за 1 кг должен быть больше 0"):
            LogisticCalculator.calculate(
                shipment=shipment,
            )

    # проверка нулевой стоимости тарифа объема
    def test_zero_tariff_one_m3(self):
        shipment = SimpleNamespace(
            logistic_calculation_type=LogisticCalculationMethod.VOLUME,
            volume=Decimal("0.035"),
            tariff_one_m3=Decimal(0),
        )

        with self.assertRaisesRegex(ValueError, "Тариф за 1 м3 должен быть больше 0"):
            LogisticCalculator.calculate(
                shipment=shipment,
            )

    # проверка неизвестного способа расчета
    def test_unknown_calculation_method(self):
        shipment = SimpleNamespace(logistic_calculation_type="unknown")

        with self.assertRaisesRegex(ValueError, "Неизвестный способ расчета"):
            LogisticCalculator.calculate(
                shipment=shipment,
            )

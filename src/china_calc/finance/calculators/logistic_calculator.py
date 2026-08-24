from decimal import Decimal

from china_calc.finance.calculators.currency_calculator import CurrencyCalculator
from config.model_choices import Currency, LogisticCalculationMethod


class LogisticCalculator:
    """
    Общая стоимость логистики всей поставки
    """

    @classmethod
    def validate(cls, shipment):
        calculation_type = shipment.logistic_calculation_type

        if calculation_type == LogisticCalculationMethod.WEIGHT:
            if shipment.weight <= Decimal("0"):
                raise ValueError("Вес поставки должен быть больше 0")

            if shipment.tariff_one_kg <= Decimal("0"):
                raise ValueError("Тариф за 1 кг должен быть больше 0")

            return

        if calculation_type == LogisticCalculationMethod.VOLUME:
            if shipment.volume <= Decimal("0"):
                raise ValueError("Объем поставки должен быть больше 0")

            if shipment.tariff_one_m3 <= Decimal("0"):
                raise ValueError("Тариф за 1 м3 должен быть больше 0")

            return

    @classmethod
    def calculate_tariff_amount(cls, shipment):
        """
        Стоимость логистики до конвертации.

        """
        cls.validate(shipment)

        if shipment.logistic_calculation_type == LogisticCalculationMethod.WEIGHT:
            return shipment.weight * shipment.tariff_one_kg

        if shipment.logistic_calculation_type == LogisticCalculationMethod.VOLUME:
            return shipment.volume * shipment.tariff_one_m3

        raise ValueError("Неизвестный способ расчета логистики")

    @classmethod
    def calculate(cls, shipment):
        """
        Стоимость логистики в итоговой валюте.
        """
        cls.validate(shipment=shipment)

        if shipment.logistic_calculation_type == LogisticCalculationMethod.WEIGHT:
            amount = shipment.weight * shipment.tariff_one_kg

        elif shipment.logistic_calculation_type == LogisticCalculationMethod.VOLUME:
            amount = shipment.volume * shipment.tariff_one_m3

        else:
            raise ValueError("Неизвестный способ расчета логистики")

        return CurrencyCalculator.convert_for_route(
            amount=amount,
            purchase_currency=shipment.tariff_currency,
            route_type=shipment.route_type,
            exchange_rate=shipment.exchange_rate,
            for_client=False,
        )

    @classmethod
    def calculate_rub(cls, shipment):
        """
        Общая доставка в RUB для внутренней информации
        """

        amount = cls.calculate_tariff_amount(shipment=shipment)

        return CurrencyCalculator.convert_currency(
            amount=amount,
            purchase_currency=shipment.tariff_currency,
            final_currency=Currency.RUB,
            exchange_rate=shipment.exchange_rate,
            for_client=False,
        )

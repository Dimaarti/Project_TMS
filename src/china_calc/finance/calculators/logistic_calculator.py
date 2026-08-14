from china_calc.finance.calculators.currency_calculator import CurrencyCalculator
from config.model_choices import LogisticCalculationMethod


class LogisticCalculator:
    """
    Общая стоимость логистики всей поставки
    """

    @classmethod
    def validate(cls, shipment):
        calculation_type = shipment.logistic_calculation_type

        if calculation_type == LogisticCalculationMethod.WEIGHT:
            if shipment.weight <= 0:
                raise ValueError("Вес поставки должен быть больше 0")

            if shipment.tariff_one_kg <= 0:
                raise ValueError("Тариф за 1 кг должен быть больше 0")

            return

        if calculation_type == LogisticCalculationMethod.VOLUME:
            if shipment.volume <= 0:
                raise ValueError("Объем поставки должен быть больше 0")

            if shipment.tariff_one_m3 <= 0:
                raise ValueError("Тариф за 1 м3 должен быть больше 0")

            return

    @classmethod
    def calculate(cls, shipment):
        cls.validate(shipment=shipment)

        if shipment.logistic_calculation_type == LogisticCalculationMethod.WEIGHT:
            amount = shipment.weight * shipment.tariff_one_kg

        elif shipment.logistic_calculation_type == LogisticCalculationMethod.VOLUME:
            amount = shipment.volume * shipment.tariff_one_m3

        else:
            raise ValueError("Неизвестный способ расчета логистики")

        return CurrencyCalculator.convert_currency(
            amount=amount,
            purchase_currency=shipment.tariff_currency,
            final_currency=shipment.settlement_final_currency,
            exchange_rate=shipment.exchange_rate,
            for_client=False,
        )

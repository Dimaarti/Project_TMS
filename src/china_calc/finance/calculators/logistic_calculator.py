from china_calc.finance.calculators.currency_calculator import CurrencyCalculator


class Logistic:
    @staticmethod
    def calculate_weight(shipment, for_client=False):
        amount = shipment.weight * shipment.tariff_one_kg

        return CurrencyCalculator.convert_currency(
            amount=amount,
            base_currency=shipment.tariff_currency,
            counter_currency=shipment.settlement_final_currency,
            exchange_rate=shipment.exchange_rate,
            for_client=for_client,
        )

    @staticmethod
    def calculate_volume(shipment, for_client=False):
        amount = shipment.volume * shipment.tariff_one_m3

        return CurrencyCalculator.convert_currency(
            amount=amount,
            base_currency=shipment.tariff_currency,
            counter_currency=shipment.settlement_final_currency,
            exchange_rate=shipment.exchange_rate,
            for_client=for_client,
        )


class LogisticCalculator:
    @staticmethod
    def calculate(shipment, for_client=False):
        calculation_type = shipment.logistic_calculation_type

        weight_cost = Logistic.calculate_weight(shipment, for_client=for_client)
        volume_cost = Logistic.calculate_volume(shipment, for_client=for_client)

        if calculation_type == "weight":
            return weight_cost

        if calculation_type == "volume":
            return volume_cost

        raise ValueError("Неизвестный способ расчета")

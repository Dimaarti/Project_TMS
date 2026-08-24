from decimal import Decimal


class ProfitCostCalculator:
    """
    Рассчитывает прибыль.
    """

    @staticmethod
    def calculate(client_price_cost, price_cost):

        if client_price_cost < Decimal("0"):
            raise ValueError("Клиентская стоимость не может быть отрицательной")

        if price_cost < Decimal("0"):
            raise ValueError("Себестоимость не может быть отрицательной")

        return client_price_cost - price_cost

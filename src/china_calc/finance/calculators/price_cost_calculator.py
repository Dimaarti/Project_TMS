from decimal import Decimal


class PriceCostCalculator:
    """
    Рассчитывает себестоимость.
    """

    @staticmethod
    def calculate(purchase_cost, logistics_cost, expenses_cost):
        components = [purchase_cost, logistics_cost, expenses_cost]

        if any(component < Decimal("0") for component in components):
            raise ValueError("Составляющие себестоимости не могут быть отрицательными")

        return purchase_cost + logistics_cost + expenses_cost

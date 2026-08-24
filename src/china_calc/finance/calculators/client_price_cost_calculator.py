from decimal import Decimal


class ClientPriceCostCalculator:
    """
    Рассчитывает итоговую стоимость для клиента.
    """

    @staticmethod
    def calculate(
        client_purchase_cost, logistics_cost, expenses_cost, buyer_commission_cost
    ):
        components = [
            client_purchase_cost,
            logistics_cost,
            expenses_cost,
            buyer_commission_cost,
        ]

        if any(component < Decimal(0) for component in components):
            raise ValueError(
                "Составляющие клиентской стоимости не могут быть отрицательными"
            )

        return (
            client_purchase_cost + logistics_cost + expenses_cost + buyer_commission_cost
        )

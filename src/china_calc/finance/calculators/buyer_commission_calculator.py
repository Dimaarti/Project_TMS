from collections import defaultdict
from decimal import Decimal

from china_calc.finance.calculators.purchase_calculator import PurchaseCalculator


class BuyerCommissionCalculator:
    """
    Рассчитывает комиссию байера отдельно по каждому клиенту.

    Комиссия применяется к общей стоимости всех товаров клиента,
    рассчитанной по клиентскому курсу.
    """

    @classmethod
    def calculate(cls, shipment, items=None, client_purchase_costs=None):
        if items is None:
            items = list(shipment.items.select_related("client").order_by("pk"))
        else:
            items = list(items)

        if not items:
            return {"total_commission_cost": Decimal("0"), "clients": {}}

        purchase_cost_client = defaultdict(
            lambda: Decimal("0"),
        )

        clients = {}
        client_results = {}
        total_commission_cost = Decimal("0")

        for item in items:
            client_purchase_cost = (
                client_purchase_costs[item.pk]
                if client_purchase_costs is not None
                else PurchaseCalculator.calculate_item(
                    item=item, shipment=shipment, for_client=True
                )
            )

            purchase_cost_client[item.client_id] += client_purchase_cost
            clients[item.client_id] = item.client

        for client_id, client_purchase_cost in purchase_cost_client.items():
            client = clients[client_id]

            commission_percent = client.buyer_commission_percent or Decimal(0)

            buyer_commission_cost = cls.calculate_amount(
                client_purchase_cost=client_purchase_cost,
                commission_percent=commission_percent,
            )

            client_results[client_id] = {
                "client_id": client_id,
                "client_purchase_cost": client_purchase_cost,
                "commission_percent": commission_percent,
                "buyer_commission_cost": buyer_commission_cost,
            }

            total_commission_cost += buyer_commission_cost

        return {
            "total_commission_cost": total_commission_cost,
            "clients": client_results,
        }

    @staticmethod
    def calculate_amount(client_purchase_cost, commission_percent):
        """
        Рассчитывает комиссию от готовой стоимости товаров клиента.
        """

        if client_purchase_cost < Decimal("0"):
            raise ValueError("Стоимость товаров клиента не может быть отрицательной")

        if commission_percent < Decimal("0"):
            raise ValueError("Процент комиссии не может быть отрицательным")

        if commission_percent > Decimal("100"):
            raise ValueError("Процент комиссии не может быть больше 100")

        return client_purchase_cost * commission_percent / Decimal("100")

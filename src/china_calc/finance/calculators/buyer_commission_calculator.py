from china_calc.finance.calculators.purchase_calculator import PurchaseCalculator


class BuyerCommissionCalculator:
    @staticmethod
    def calculate_item(item, shipment):
        client_purchase_cost = PurchaseCalculator.calculate_item(
            item=item,
            shipment=shipment,
            for_client=True,
        )

        commission_percent = item.client.buyer_commission_percent or 0

        commission = client_purchase_cost * commission_percent / 100
        return commission

    @staticmethod
    def calculate(shipment):
        total_commission = 0

        items = shipment.item.select_related("client")

        for item in items:
            item_commission = BuyerCommissionCalculator.calculate_item(
                item=item,
                shipment=shipment,
            )

            total_commission += item_commission

        return total_commission

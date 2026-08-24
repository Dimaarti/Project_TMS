from decimal import Decimal

from django.db import transaction

from china_calc.finance.calculators.buyer_commission_calculator import (
    BuyerCommissionCalculator,
)
from china_calc.finance.calculators.client_price_cost_calculator import (
    ClientPriceCostCalculator,
)
from china_calc.finance.calculators.logistic_allocation_calculator import (
    LogisticAllocationCalculator,
)
from china_calc.finance.calculators.logistic_calculator import LogisticCalculator
from china_calc.finance.calculators.price_cost_calculator import PriceCostCalculator
from china_calc.finance.calculators.profit_calculate import ProfitCostCalculator
from china_calc.finance.calculators.purchase_calculator import PurchaseCalculator
from china_calc.finance.calculators.shipment_expense_calculator import (
    ShipmentExpenseCalculator,
)
from china_calc.finance.models.calculation_result import CalculationResult
from china_calc.finance.models.client_calculation_result import ClientCalculationResult
from china_calc.finance.models.item_calculation_result import ItemCalculationResult
from config.model_choices import DeliveryRouteType, ShipmentStatus


class ShipmentCalculatorService:
    @classmethod
    @transaction.atomic
    def calculate(
        cls,
        shipment,
    ):
        shipment.settlement_final_currency = shipment.route_final_currency
        items = list(shipment.items.select_related("client").order_by("pk"))

        if not items:
            raise ValueError("В поставке отсутствуют товары.")

        expenses_source = list(shipment.expenses.select_related("item").order_by("pk"))

        purchase_costs = {
            item.pk: PurchaseCalculator.calculate_item(
                item=item, shipment=shipment, for_client=False
            )
            for item in items
        }
        client_purchase_costs = {
            item.pk: PurchaseCalculator.calculate_item(
                item=item, shipment=shipment, for_client=True
            )
            for item in items
        }

        logistics = LogisticAllocationCalculator.calculate(
            shipment=shipment,
            items=items,
        )

        expenses = ShipmentExpenseCalculator.calculate(
            shipment=shipment,
            items=items,
            expenses=expenses_source,
        )

        logistics_cost_rub = Decimal(0)
        if shipment.route_type == DeliveryRouteType.CHINA_RUSSIA_BELARUS:
            logistics_cost_rub = (
                LogisticCalculator.calculate_rub(shipment=shipment)
                + expenses["total_expenses_cost_rub"]
            )

        commissions = BuyerCommissionCalculator.calculate(
            shipment=shipment,
            items=items,
            client_purchase_costs=client_purchase_costs,
        )

        purchase_cost = sum(purchase_costs.values(), Decimal(0))

        client_purchase_cost = sum(client_purchase_costs.values(), Decimal(0))

        price_cost = PriceCostCalculator.calculate(
            purchase_cost=purchase_cost,
            logistics_cost=logistics.logistics_cost,
            expenses_cost=expenses["total_expenses_cost"],
        )

        client_price_cost = ClientPriceCostCalculator.calculate(
            client_purchase_cost=client_purchase_cost,
            logistics_cost=logistics.logistics_cost,
            expenses_cost=expenses["total_expenses_cost"],
            buyer_commission_cost=commissions["total_commission_cost"],
        )

        profit_cost = ProfitCostCalculator.calculate(
            client_price_cost=client_price_cost,
            price_cost=price_cost,
        )

        shipment.invalidate_calculations()

        calculation_result = CalculationResult.objects.create(
            shipment=shipment,
            exchange_rate=shipment.exchange_rate,
            final_currency=shipment.settlement_final_currency,
            purchase_cost=purchase_cost,
            client_purchase_cost=client_purchase_cost,
            logistics_cost=logistics.logistics_cost,
            logistics_cost_rub=logistics_cost_rub,
            expenses_cost=expenses["total_expenses_cost"],
            buyer_commission_cost=commissions["total_commission_cost"],
            price_cost=price_cost,
            client_price_cost=client_price_cost,
            profit_cost=profit_cost,
            is_actual=True,
        )

        client_results = cls.create_client_results(
            items=items,
            calculation_result=calculation_result,
            logistics=logistics,
            expenses=expenses,
            commissions=commissions,
            purchase_costs=purchase_costs,
            client_purchase_costs=client_purchase_costs,
        )

        cls.create_item_results(
            items=items,
            client_results=client_results,
            logistics=logistics,
            expenses=expenses,
            purchase_costs=purchase_costs,
            client_purchase_costs=client_purchase_costs,
        )

        shipment.status = ShipmentStatus.CALCULATED
        shipment.save(update_fields=["status", "updated_at"])

        return calculation_result

    @staticmethod
    def create_client_results(
        items,
        calculation_result,
        logistics,
        expenses,
        commissions,
        purchase_costs,
        client_purchase_costs,
    ):
        clients = {item.client_id: item.client for item in items}
        item_ids_by_client = {client_id: [] for client_id in clients}

        for item in items:
            item_ids_by_client[item.client_id].append(item.pk)

        results = {}

        for client_id, client in clients.items():
            client_item_ids = item_ids_by_client[client_id]
            purchase_cost = sum(
                (purchase_costs[item_id] for item_id in client_item_ids),
                Decimal(0),
            )
            client_purchase_cost = sum(
                (client_purchase_costs[item_id] for item_id in client_item_ids),
                Decimal(0),
            )

            logistics_cost = logistics.clients[client_id].logistics_cost

            expenses_cost = expenses["clients"][client_id]["total_expenses_cost"]

            commission = commissions["clients"][client_id]

            buyer_commission_cost = commission["buyer_commission_cost"]

            price_cost = PriceCostCalculator.calculate(
                purchase_cost=purchase_cost,
                logistics_cost=logistics_cost,
                expenses_cost=expenses_cost,
            )

            client_price_cost = ClientPriceCostCalculator.calculate(
                client_purchase_cost=client_purchase_cost,
                logistics_cost=logistics_cost,
                expenses_cost=expenses_cost,
                buyer_commission_cost=buyer_commission_cost,
            )

            profit_cost = ProfitCostCalculator.calculate(
                client_price_cost=client_price_cost,
                price_cost=price_cost,
            )

            results[client_id] = ClientCalculationResult.objects.create(
                calculation_result=calculation_result,
                client=client,
                commission_percent=commission["commission_percent"],
                purchase_cost=purchase_cost,
                client_purchase_cost=client_purchase_cost,
                logistics_cost=logistics_cost,
                expenses_cost=expenses_cost,
                buyer_commission_cost=buyer_commission_cost,
                price_cost=price_cost,
                client_price_cost=client_price_cost,
                profit_cost=profit_cost,
            )

        return results

    @staticmethod
    def create_item_results(
        items,
        client_results,
        logistics,
        expenses,
        purchase_costs,
        client_purchase_costs,
    ):
        results = []

        for item in items:
            purchase_cost = purchase_costs[item.pk]
            client_purchase_cost = client_purchase_costs[item.pk]

            item_logistics = logistics.items[item.pk]

            item_expenses = expenses["items"][item.pk]

            total_cost = PriceCostCalculator.calculate(
                purchase_cost=client_purchase_cost,
                logistics_cost=item_logistics.logistics_cost,
                expenses_cost=item_expenses["total_expenses_cost"],
            )

            results.append(
                ItemCalculationResult(
                    client_result=client_results[item.client_id],
                    item=item,
                    purchase_cost=purchase_cost,
                    client_purchase_cost=client_purchase_cost,
                    allocation_basis=item_logistics.basis,
                    allocation_ratio=item_logistics.ratio,
                    logistics_cost=item_logistics.logistics_cost,
                    direct_expenses_cost=item_expenses["direct_expenses_cost"],
                    distributed_expenses_cost=item_expenses["distributed_expenses_cost"],
                    total_cost=total_cost,
                )
            )
        return ItemCalculationResult.objects.bulk_create(results)

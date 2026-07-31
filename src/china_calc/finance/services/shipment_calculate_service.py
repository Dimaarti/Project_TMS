from china_calc.finance.calculators.additional_services_calculator import (
    AdditionalServicesCalculators,
)
from china_calc.finance.calculators.buyer_commission_calculator import (
    BuyerCommissionCalculator,
)
from china_calc.finance.calculators.client_price_cost_calculator import (
    ClientPriceCostCalculator,
)
from china_calc.finance.calculators.logistic_calculator import LogisticCalculator
from china_calc.finance.calculators.price_cost_calculator import PriceCostCalculator
from china_calc.finance.calculators.profit_calculate import ProfitCostCalculator
from china_calc.finance.calculators.purchase_calculator import PurchaseCalculator
from china_calc.finance.models.calculation_result import CalculationResult
from config.model_choices import Currency


class ShipmentCalculatorService:
    @staticmethod
    def calculate(shipment):
        purchase_cost = PurchaseCalculator.calculate(shipment)
        client_purchase_cost = PurchaseCalculator.calculate(shipment, for_client=True)
        logistics_cost = LogisticCalculator.calculate(shipment)
        additional_services = AdditionalServicesCalculators.calculate(shipment)
        buyer_commission_cost = BuyerCommissionCalculator.calculate(shipment)
        price_cost = PriceCostCalculator.calculate(shipment)
        client_price_cost = ClientPriceCostCalculator.calculate(shipment)
        profit_cost = ProfitCostCalculator.calculate(client_price_cost, price_cost)

        calculation_result = CalculationResult.objects.update_or_create(
            shipment=shipment,
            defaults={
                "exchange_rate": shipment.exchange_rate,
                "base_currency": Currency.CNY,
                "counter_currency": shipment.settlement_final_currency,
                "purchase_cost": purchase_cost,
                "client_purchase_cost": client_purchase_cost,
                "logistics_cost": logistics_cost,
                "additional_services": additional_services,
                "buyer_commission_cost": buyer_commission_cost,
                "price_cost": price_cost,
                "client_price_cost": client_price_cost,
                "profit_cost": profit_cost,
            },
        )
        return calculation_result

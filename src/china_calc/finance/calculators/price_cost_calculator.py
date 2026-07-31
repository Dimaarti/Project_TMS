from china_calc.finance.calculators.additional_services_calculator import (
    AdditionalServicesCalculators,
)
from china_calc.finance.calculators.logistic_calculator import LogisticCalculator
from china_calc.finance.calculators.purchase_calculator import PurchaseCalculator


class PriceCostCalculator:
    @staticmethod
    def calculate(shipment):
        purchase_cost = PurchaseCalculator.calculate(shipment)
        logistics_cost = LogisticCalculator.calculate(shipment)
        additional_services = AdditionalServicesCalculators.calculate(shipment)
        return purchase_cost + logistics_cost + additional_services

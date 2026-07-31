from china_calc.finance.calculators.additional_services_calculator import (
    AdditionalServicesCalculators,
)
from china_calc.finance.calculators.buyer_commission_calculator import (
    BuyerCommissionCalculator,
)
from china_calc.finance.calculators.logistic_calculator import LogisticCalculator
from china_calc.finance.calculators.purchase_calculator import PurchaseCalculator


class ClientPriceCostCalculator:
    @staticmethod
    def calculate(shipment):
        client_purchase_cost = PurchaseCalculator.calculate(shipment, for_client=True)
        logistic_cost = LogisticCalculator.calculate(shipment)
        additional_services_cost = AdditionalServicesCalculators.calculate(shipment)
        buyer_commission_cost = BuyerCommissionCalculator.calculate(shipment)
        return (
            client_purchase_cost
            + logistic_cost
            + additional_services_cost
            + buyer_commission_cost
        )

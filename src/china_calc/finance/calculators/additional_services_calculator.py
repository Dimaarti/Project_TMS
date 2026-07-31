from china_calc.finance.calculators.currency_calculator import CurrencyCalculator


class AdditionalServicesCalculators:
    @staticmethod
    def calculate(shipment, for_client=False):
        result = 0

        for item in shipment.item.all():
            result += (
                item.inspection_cost + item.photo_report_cost + item.packaging_cost
            )
        expenses = shipment.expense.all()

        for expense in expenses:
            result += CurrencyCalculator.convert_currency(
                amount=expense.amount,
                base_currency=expense.currency,
                counter_currency=shipment.settlement_final_currency,
                exchange_rate=shipment.exchange_rate,
                for_client=for_client,
            )
        return result

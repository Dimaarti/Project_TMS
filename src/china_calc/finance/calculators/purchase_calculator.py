from china_calc.finance.calculators.currency_calculator import CurrencyCalculator


class PurchaseCalculator:
    @staticmethod
    def calculate_item(item, shipment, for_client=False):
        amount = item.price * item.quantity
        return CurrencyCalculator.convert_currency(
            amount=amount,
            base_currency=item.price_currency,
            counter_currency=shipment.settlement_final_currency,
            exchange_rate=shipment.exchange_rate,
            for_client=for_client,
        )

    @staticmethod
    def calculate(shipment, for_client=False):
        return sum(
            PurchaseCalculator.calculate_item(
                item=item,
                shipment=shipment,
                for_client=for_client,
            )
            for item in shipment.item.all()
        )

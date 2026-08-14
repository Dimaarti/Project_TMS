from china_calc.finance.calculators.currency_calculator import CurrencyCalculator


class PurchaseCalculator:
    @staticmethod
    def calculate_item(item, shipment, for_client=False):
        """
        Рассчитывает стоимость одной товарной позиции.
        for_client = True - стоимость по клиентскому курсу.
        for_client = False - по курсу себестоимости.
        """
        if item.price < 0:
            raise ValueError("Цена товара не может быть отрицательной")
        if item.quantity <= 0:
            raise ValueError("Количество товара должно быть больше 0")

        amount = item.price * item.quantity

        return CurrencyCalculator.convert_currency(
            amount=amount,
            purchase_currency=item.price_currency,
            final_currency=shipment.settlement_final_currency,
            exchange_rate=shipment.exchange_rate,
            for_client=for_client,
        )

    @classmethod
    def calculate_items(
        cls,
        items,
        shipment,
        for_client=False,
    ):
        """
        Рассчитывает стоимость набора товаров.
        """
        return sum(
            cls.calculate_item(
                item=item,
                shipment=shipment,
                for_client=for_client,
            )
            for item in items
        )

    @classmethod
    def calculate_shipment(
        cls,
        shipment,
        for_client=False,
    ):
        """
        Рассчитывает стоимость всех товаров поставки
        """
        return cls.calculate_items(
            items=shipment.items.all(),
            shipment=shipment,
            for_client=for_client,
        )

    @classmethod
    def calculate_client(
        cls,
        shipment,
        client,
        for_client=False,
    ):
        """
        Рассчитывает стоимость товаров конкретного клиента в конкретной поставке
        """
        items = shipment.items.filter(client=client)

        return cls.calculate_items(
            items=items,
            shipment=shipment,
            for_client=for_client,
        )

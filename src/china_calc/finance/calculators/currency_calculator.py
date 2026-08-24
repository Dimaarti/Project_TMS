from decimal import Decimal
from typing import ClassVar

from config.model_choices import Currency, DeliveryRouteType


class CurrencyCalculator:
    fields: ClassVar[dict] = {
        (Currency.CNY, Currency.BYN): "cny_to_byn",
        (Currency.CNY, Currency.RUB): "cny_to_rub",
        (Currency.USD, Currency.BYN): "usd_to_byn",
        (Currency.USD, Currency.RUB): "usd_to_rub",
        (Currency.RUB, Currency.BYN): "rub_to_byn",
    }

    inverse_fields: ClassVar[dict] = {
        (Currency.BYN, Currency.RUB): "rub_to_byn",
    }

    route_targets: ClassVar[dict] = {
        DeliveryRouteType.CHINA_RUSSIA: (Currency.RUB,),
        DeliveryRouteType.CHINA_BELARUS: (Currency.BYN,),
        DeliveryRouteType.CHINA_RUSSIA_BELARUS: (Currency.RUB, Currency.BYN),
    }

    @staticmethod
    def convert_currency(
        amount, purchase_currency, final_currency, exchange_rate, for_client=False
    ):
        """
        Переводит сумму в итоговую валюту.

        for_client = True, используется только для стоимости товаров.
        Для логистики и расходов, курс себестоимости.
        """

        if amount < Decimal(0):
            raise ValueError("Сумма не может быть отрицательной")

        if purchase_currency == final_currency:
            return amount

        field = CurrencyCalculator.fields.get((purchase_currency, final_currency))

        is_inverse = False

        if field is None:
            field = CurrencyCalculator.inverse_fields.get(
                purchase_currency, final_currency
            )
            is_inverse = field is not None

        if field is None:
            raise ValueError("Конвертация не поддерживается")

        if for_client:
            field = f"{field}_client"

        rate = getattr(exchange_rate, field, None)

        if rate is None:
            raise ValueError(f"В модели обменного курса отсутствует поле {field}")

        if rate <= 0:
            raise ValueError("Курс не может быть отрицательным")

        if is_inverse:
            return amount / rate

        return amount * rate

    @classmethod
    def convert_for_route(
        cls, amount, purchase_currency, route_type, exchange_rate, for_client=False
    ):
        if amount < Decimal(0):
            raise ValueError("Сумма не может быть отрицательной")

        targets = cls.route_targets.get(route_type)

        if targets is None:
            raise ValueError("Неизвестный маршрут")

        final_currency = targets[-1]

        if purchase_currency == final_currency:
            return amount

        converted_amount = amount
        current_currency = purchase_currency

        for target_currency in targets:
            if current_currency == target_currency:
                continue

            converted_amount = cls.convert_currency(
                amount=converted_amount,
                purchase_currency=current_currency,
                final_currency=target_currency,
                exchange_rate=exchange_rate,
                for_client=for_client,
            )

            current_currency = target_currency

        return converted_amount

    @classmethod
    def convert_goods(
        cls, amount, purchase_currency, final_currency, exchange_rate, for_client=False
    ):
        """
        Конвертация стоимости товаров.

        Разрешены:
        CNY -> RUB
        CNY -> BYN
        """

        if amount < Decimal(0):
            raise ValueError("Стоимость товара не может быть отрицательной")

        if purchase_currency == final_currency:
            return amount

        if purchase_currency != Currency.CNY:
            raise ValueError("Исходной валютой стоимости должен быть CNY")

        if final_currency not in (Currency.RUB, Currency.BYN):
            raise ValueError("Стоимость товара можно конвертировать только в RUB или BYN")

        return cls.convert_currency(
            amount=amount,
            purchase_currency=Currency.CNY,
            final_currency=final_currency,
            exchange_rate=exchange_rate,
            for_client=for_client,
        )

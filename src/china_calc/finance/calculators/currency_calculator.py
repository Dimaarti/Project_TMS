from config.model_choices import Currency


class CurrencyCalculator:
    fields = {
        (Currency.CNY, Currency.BYN): "cny_to_byn",
        (Currency.CNY, Currency.RUB): "cny_to_rub",
        (Currency.USD, Currency.BYN): "usd_to_byn",
        (Currency.USD, Currency.RUB): "usd_to_rub",
        (Currency.RUB, Currency.BYN): "rub_to_byn",
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

        if amount < 0:
            raise ValueError("Сумма не может быть отрицательной")

        if purchase_currency == final_currency:
            return amount

        field = CurrencyCalculator.fields.get(
            (purchase_currency, final_currency)
        )

        if field is None:
            raise ValueError("Конвертация не поддерживается")

        if for_client:
            field = f"{field}_client"

        rate = getattr(exchange_rate, field, None)

        if rate is None:
            raise ValueError(f"В модели обменного курса отсутствует поле - {field}")

        if rate <= 0:
            raise ValueError("Курс должен быть больше 0")

        return amount * rate

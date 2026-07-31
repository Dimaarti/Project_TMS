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
        amount, base_currency, counter_currency, exchange_rate, for_client
    ):
        if base_currency == counter_currency:
            return amount

        field = CurrencyCalculator.fields.get((base_currency, counter_currency))

        if field is None:
            raise ValueError("Конвертация не поддерживается")

        if for_client:
            field = f"{field}_client"

        rate = getattr(exchange_rate, field)

        if rate <= 0:
            raise ValueError("Курс не может быть меньше или равен 0")
        return amount * rate

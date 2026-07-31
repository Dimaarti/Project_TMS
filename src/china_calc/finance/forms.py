from django import forms

from china_calc.finance.models.calculation_result import CalculationResult
from china_calc.finance.models.exchange_rate import ExchangeRate


class ShipmentCalculateForm(forms.ModelForm):
    class Meta:
        model = CalculationResult
        fields = [
            "exchange_rate",
            "base_currency",
            "counter_currency",
            "purchase_cost",
            "client_purchase_cost",
            "logistics_cost",
            "buyer_commission_cost",
            "price_cost",
            "client_price_cost",
            "profit_cost",
            "additional_services",
        ]


class ExchangeRateForm(forms.ModelForm):
    class Meta:
        model = ExchangeRate
        fields = [
            "date",
            "cny_to_byn",
            "cny_to_byn_client",
            "cny_to_rub",
            "cny_to_rub_client",
            "usd_to_byn",
            "usd_to_byn_client",
            "usd_to_rub",
            "usd_to_rub_client",
            "rub_to_byn",
            "rub_to_byn_client",
        ]

        widgets = {
            "date": forms.DateInput(attrs={"type": "date"}),
            "cny_to_byn": forms.NumberInput(attrs={"type": "number"}),
            "cny_to_byn_client": forms.NumberInput(attrs={"type": "number"}),
            "cny_to_rub": forms.NumberInput(attrs={"type": "number"}),
            "cny_to_rub_client": forms.NumberInput(attrs={"type": "number"}),
            "usd_to_byn": forms.NumberInput(attrs={"type": "number"}),
            "usd_to_byn_client": forms.NumberInput(attrs={"type": "number"}),
            "usd_to_rub": forms.NumberInput(attrs={"type": "number"}),
            "usd_to_rub_client": forms.NumberInput(attrs={"type": "number"}),
            "rub_to_byn": forms.NumberInput(attrs={"type": "number"}),
            "rub_to_byn_client": forms.NumberInput(attrs={"type": "number"}),
        }

from django import forms

from china_calc.finance.models.exchange_rate import ExchangeRate


class ExchangeRateForm(forms.ModelForm):
    def __init__(self, user=None,  *args, **kwargs):
        super().__init__(*args, **kwargs)
        if user is not None and not self.instance.pk:
            self.instance.user = user

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

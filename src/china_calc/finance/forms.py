from django import forms

from china_calc.finance.models import ClientPayment
from china_calc.finance.models.exchange_rate import ExchangeRate


class ExchangeRateForm(forms.ModelForm):
    def __init__(self, user=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if user is not None and not self.instance.pk:
            self.instance.user = user

    def clean(self):
        cleaned_data = super().clean()

        for field_name in self.Meta.fields:
            if field_name == "date":
                continue

            value = cleaned_data.get(field_name)
            if value is not None and value <= 0:
                self.add_error(field_name, "Курс должен быть больше 0")

        return cleaned_data

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
            "date": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
        }


class ClientPaymentForm(forms.ModelForm):
    class Meta:
        model = ClientPayment
        fields = ["amount", "note"]

        widgets = {
            "amount": forms.NumberInput(
                attrs={"type": "number", "class": "form-control"}
            ),
            "note": forms.Textarea(attrs={"rows": 3, "class": "form-control"}),
        }

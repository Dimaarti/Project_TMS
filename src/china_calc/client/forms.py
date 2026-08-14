from django import forms

from china_calc.client.models import Client


class ClientForm(forms.ModelForm):
    def clean_full_name(self):
        return self.cleaned_data["full_name"]
    def clean_phone(self):
        return self.cleaned_data["phone"]

    class Meta:
        model = Client
        fields = [
            "full_name",
            "phone",
            "address",
            "buyer_commission_percent",
        ]

        widgets = {
            "full_name": forms.TextInput(attrs={"class": "form-control"}),
            "phone": forms.TextInput(attrs={"class": "form-control"}),
            "address": forms.TextInput(attrs={"class": "form-control"}),
            "buyer_commission_percent": forms.NumberInput(
                attrs={"class": "form-control"}
            ),
        }

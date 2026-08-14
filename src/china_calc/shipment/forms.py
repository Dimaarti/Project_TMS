from django import forms

from china_calc.shipment.models import Shipment, ShipmentExpense, ShipmentItem


class ShipmentForm(forms.ModelForm):
    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user is not None:
            self.fields["exchange_rate"].queryset = user.exchange_rates.all()

    class Meta:
        model = Shipment
        fields = [
            "number",
            "route",
            "exchange_rate",
            "tariff_one_kg",
            "tariff_one_m3",
            "tariff_currency",
            "settlement_final_currency",
            "status",
            "logistic_calculation_type",
            "note",
        ]

        widgets = {
            "number": forms.TextInput(attrs={"class": "form-control"}),
            "route": forms.Select(attrs={"class": "form-select"}),
            "exchange_rate": forms.Select(attrs={"class": "form-select"}),
            "tariff_one_kg": forms.NumberInput(attrs={"class": "form-control"}),
            "tariff_one_m3": forms.NumberInput(attrs={"class": "form-control"}),
            "tariff_currency": forms.Select(attrs={"class": "form-select"}),
            "settlement_final_currency": forms.Select(attrs={"class": "form-select"}),
            "status": forms.Select(attrs={"class": "form-select"}),
            "logistic_calculation_type": forms.Select(attrs={"class": "form-select"}),
            "note": forms.Textarea(attrs={"class": "form-control"}),
        }


class ShipmentItemForm(forms.ModelForm):
    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user is not None:
            self.fields["client"].queryset = user.clients.all()

    class Meta:
        model = ShipmentItem
        fields = [
            "client",
            "name",
            "product_link",
            "tracking_number",
            "quantity",
            "price",
            "price_currency",
            "weight",
            "volume",
        ]

        widgets = {
            "client": forms.Select(attrs={"class": "form-select"}),
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "product_link": forms.URLInput(attrs={"class": "form-control"}),
            "tracking_number": forms.TextInput(attrs={"class": "form-control"}),
            "quantity": forms.NumberInput(attrs={"class": "form-control"}),
            "price": forms.NumberInput(attrs={"class": "form-control"}),
            "price_currency": forms.Select(attrs={"class": "form-select"}),
            "weight": forms.NumberInput(attrs={"class": "form-control"}),
            "volume": forms.NumberInput(attrs={"class": "form-control"}),
        }


class ShipmentExpenseForm(forms.ModelForm):
    def __init__(self, *args, shipment=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.shipment = shipment

        if shipment is not None:
            self.fields["item"].queryset = shipment.items.all()


    class Meta:
        model = ShipmentExpense
        fields = ["item", "expense_type", "amount", "currency", "note"]

        widgets = {
            "item": forms.Select(attrs={"class": "form-select"}),
            "expense_type": forms.Select(attrs={"class": "form-select"}),
            "amount": forms.NumberInput(attrs={"class": "form-control"}),
            "currency": forms.Select(attrs={"class": "form-select"}),
            "note": forms.Textarea(attrs={"class": "form-control"}),
        }

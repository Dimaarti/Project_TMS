from django import forms

from china_calc.shipment.models import Shipment, ShipmentItem


class ShipmentForm(forms.ModelForm):
    class Meta:
        model = Shipment
        fields = [
            "number",
            "route",
            "exchange_rate",
            "tariff_one_kg",
            "tariff_currency",
            "settlement_final_currency",
            "status",
            "weight",
            "volume",
            "logistic_calculation_type",
            "tariff_one_m3",
            "note",
        ]

    widgets = {
        "number": forms.TextInput(attrs={"class": "form-control"}),
        "route": forms.Select(attrs={"class": "form-control"}),
        "exchange_rate": forms.Select(attrs={"class": "form-control"}),
        "tariff_one_kg": forms.NumberInput(attrs={"class": "form-control"}),
        "tariff_one_m3": forms.NumberInput(attrs={"class": "form-control"}),
        "settlement_final_currency": forms.TextInput(attrs={"class": "form-control"}),
        "status": forms.HiddenInput(attrs={"readonly": "readonly"}),
        "weight": forms.NumberInput(attrs={"class": "form-control"}),
        "volume": forms.NumberInput(attrs={"class": "form-control"}),
        "logistic_calculation_type": forms.Select(attrs={"class": "form-control"}),
        "tariff_currency": forms.Select(attrs={"class": "form-control"}),
        "note": forms.Textarea(attrs={"class": "form-control"}),
    }


class ItemForm(forms.ModelForm):
    class Meta:
        model = ShipmentItem
        fields = [
            "client",
            "product",
            "product_link",
            "tracking_number",
            "quantity",
            "price",
            "price_currency",
            "inspection_cost",
            "photo_report_cost",
            "packaging_cost",
        ]

        widgets = {
            "client": forms.Select(attrs={"class": "form-select"}),
            "product": forms.Select(attrs={"class": "form-select"}),
            "product_link": forms.URLInput(attrs={"class": "form-control"}),
            "tracking_number": forms.TextInput(attrs={"class": "form-control"}),
            "quantity": forms.NumberInput(attrs={"class": "form-control"}),
            "price": forms.NumberInput(attrs={"class": "form-control"}),
            "price_currency": forms.TextInput(attrs={"class": "form-control"}),
            "inspections_cost": forms.NumberInput(attrs={"class": "form-control"}),
            "photo_report_cost": forms.NumberInput(attrs={"class": "form-control"}),
            "packaging_cost": forms.NumberInput(attrs={"class": "form-control"}),
        }

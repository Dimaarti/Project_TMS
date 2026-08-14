from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.generic import CreateView, DeleteView, UpdateView

from china_calc.finance.calculators.shipment_cargo_calculator import ShipmentCargoCalculator
from china_calc.shipment.forms import ShipmentItemForm
from china_calc.shipment.models import ShipmentItem, Shipment


class ShipmentItemCreateView(LoginRequiredMixin, CreateView):
    model = ShipmentItem
    form_class = ShipmentItemForm
    template_name = "item/item_create.html"

    def dispatch(self, request, *args, **kwargs):
        self.shipment = get_object_or_404(
            Shipment,
            pk=kwargs["shipment_pk"],
            user=request.user
        )
        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs


    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.instance.shipment = self.shipment

        return form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["shipment"] = self.shipment
        context["title"] = "Новый товар"
        context["cancel_url"] = reverse(
            "shipment:detail",
            kwargs={"pk": self.shipment.pk}
        )
        return context

    def form_valid(self, form):
        form.instance.shipment = self.shipment

        response = super().form_valid(form)

        ShipmentCargoCalculator(
            shipment=self.shipment,
        ).apply()

        self.shipment.invalidate_calculations()

        messages.success(
            self.request,
            "Товар добавлен. Вес и объём поставки пересчитаны.",
        )

        return response

    def get_success_url(self):
        return reverse(
            "shipment:detail",
            kwargs={"pk": self.object.shipment_id},
        )


class ShipmentItemUpdateView(LoginRequiredMixin, UpdateView):
    model = ShipmentItem
    form_class = ShipmentItemForm
    template_name = "item/item_create.html"

    def get_queryset(self):
        return ShipmentItem.objects.filter(shipment__user=self.request.user)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Редактирование товара"
        context["shipment"] = self.object.shipment
        context["cancel_url"] = reverse(
            "shipment:detail",
            kwargs={"pk": self.object.shipment_id},
        )
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def form_valid(self, form):
        response = super().form_valid(form)

        shipment = self.object.shipment

        ShipmentCargoCalculator(
            shipment=shipment,
        ).apply()

        shipment.invalidate_calculations()

        messages.success(
            self.request,
            "Товар обновлён. Вес и объём поставки пересчитаны.",
        )

        return response

    def get_success_url(self):
        return reverse("shipment:detail", kwargs={"pk": self.object.shipment_id})




class ShipmentItemDeleteView(LoginRequiredMixin, DeleteView):
    model = ShipmentItem
    template_name = "universal_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Удаление товара"
        context["delete_mode"] = True
        context["cancel_url"] = reverse(
            "shipment:detail",
            kwargs={"pk": self.object.shipment_id},
        )
        return context



    def get_queryset(self):
        return ShipmentItem.objects.filter(shipment__user=self.request.user).select_related("shipment")

    def form_valid(self, form):
        shipment = self.object.shipment

        self.success_url = reverse(
            "shipment:detail",
            kwargs={"pk": shipment.pk},
        )

        response = super().form_valid(form)

        ShipmentCargoCalculator(
            shipment=shipment,
        ).apply()

        shipment.invalidate_calculations()

        messages.success(
            self.request,
            "Товар удалён. Вес и объём поставки пересчитаны.",
        )

        return response



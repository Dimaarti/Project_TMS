from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from china_calc.shipment.forms import ItemForm, ShipmentForm
from china_calc.shipment.models import Shipment, ShipmentItem


class ShipmentListView(LoginRequiredMixin, ListView):
    model = Shipment
    context_object_name = "shipment"
    queryset = Shipment.objects.select_related(
        "route", "exchange_rate", "calculation_result"
    ).order_by("id")
    paginate_by = 5


class ShipmentCreateView(LoginRequiredMixin, CreateView):
    model = Shipment
    form_class = ShipmentForm
    template_name = "shipment/shipment_create.html"
    success_url = reverse_lazy("shipment:list")

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class ShipmentUpdateView(LoginRequiredMixin, UpdateView):
    model = Shipment
    form_class = ShipmentForm
    template_name = "shipment/shipment_create.html"
    context_object_name = "shipment"

    def get_queryset(self):
        return Shipment.objects.filter(user=self.request.user)

    def get_success_url(self):
        return reverse("shipment:detail", kwargs={"pk": self.object.pk})


class ShipmentDetailView(LoginRequiredMixin, DetailView):
    model = Shipment
    template_name = "shipment/shipment_detail.html"
    context_object_name = "shipment"

    def get_queryset(self):
        return (
            Shipment.objects.filter(user=self.request.user)
            .select_related("route", "exchange_rate", "calculation_result")
            .prefetch_related("item__product", "item__client")
        )


class ShipmentDeleteView(LoginRequiredMixin, DeleteView):
    model = Shipment
    success_url = reverse_lazy("shipment:list")

    def get_queryset(self):
        return Shipment.objects.filter(user=self.request.user)


class ItemCreateView(LoginRequiredMixin, CreateView):
    model = ShipmentItem
    form_class = ItemForm
    template_name = "item/item_create.html"

    def get_success_url(self):
        return reverse(
            "shipment:detail",
            kwargs={"pk": self.object.shipment_id},
        )

    def form_valid(self, form):
        shipment = get_object_or_404(
            Shipment,
            pk=self.kwargs["pk"],
            user=self.request.user,
        )

        form.instance.shipment = shipment
        return super().form_valid(form)

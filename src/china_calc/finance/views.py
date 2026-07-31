from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import ProtectedError
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, DetailView, ListView

from china_calc.finance.forms import ExchangeRateForm
from china_calc.finance.models.exchange_rate import ExchangeRate
from china_calc.finance.services.shipment_calculate_service import (
    ShipmentCalculatorService,
)
from china_calc.shipment.models import Shipment


class ShipmentCalculateView(LoginRequiredMixin, View):

    def post(self, request, pk):
        shipment = get_object_or_404(
            Shipment.objects.select_related("exchange_rate"), pk=pk, user=request.user
        )

        try:
            ShipmentCalculatorService.calculate(shipment)
            messages.success(
                request,
                "Поставка успешно рассчитана",
            )

        except ValueError:
            messages.error(
                request,
                "Поставка не рассчитана")
        return redirect("shipment:detail", pk=shipment.pk)


class ExchangeRateListView(LoginRequiredMixin, ListView):
    model = ExchangeRate
    context_object_name = "exchange_rate"
    template_name = "finance/exchange_rate_list.html"



class ExchangeRateDetailView(LoginRequiredMixin, DetailView):
    model = ExchangeRate
    template_name = "finance/exchange_rate_detail.html"
    context_object_name = "rate"


class ExchangeRateDeleteView(LoginRequiredMixin, View):
    model = ExchangeRate
    success_url = reverse_lazy("finance:list")

    def post(self, request, pk):
        exchange_rate = get_object_or_404(ExchangeRate, pk=pk)

        try:
            exchange_rate.delete()
        except ProtectedError:
            messages.error(
                request,
                "Курс нельзя удалить: он используется поставках.",
            )
        else:
            messages.success(
                request,
                "Курс успешно удалён.",
            )

        return redirect("finance:list")


class ExchangeRateCreateView(LoginRequiredMixin, CreateView):
    model = ExchangeRate
    form_class = ExchangeRateForm
    template_name = "finance/exchange_rate_create.html"
    success_url = reverse_lazy("finance:list")

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import ProtectedError, Sum
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import DetailView, ListView, CreateView, DeleteView
from pygments.lexer import default

from china_calc.finance.forms import ExchangeRateForm
from china_calc.finance.models.calculation_result import CalculationResult
from china_calc.finance.models.exchange_rate import ExchangeRate
from china_calc.finance.services.shipment_calculate_service import (
    ShipmentCalculatorService,
)
from china_calc.shipment.models import Shipment


class ShipmentCalculateView(LoginRequiredMixin, View):
    def post(self, request, pk):
        shipment = get_object_or_404(
            Shipment,
            pk=pk,
            user=request.user,
        )

        try:
            result = ShipmentCalculatorService.calculate(
                shipment=shipment,
            )
        except ValueError as error:
            messages.error(
                request,
                str(error),
            )

            return redirect(
                "shipment:detail",
                pk=shipment.pk,
            )

        messages.success(
            request,
            "Расчёт поставки выполнен.",
        )

        return redirect(
            "finance:calculations_detail",
            pk=result.pk,
        )


class ExchangeRateListView(LoginRequiredMixin, ListView):
    model = ExchangeRate
    template_name = "finance/exchange_rate_list.html"
    context_object_name = "exchange_rate"

    def get_queryset(self):
        return ExchangeRate.objects.filter(user=self.request.user).order_by("-date")


class ExchangeRateDetailView(LoginRequiredMixin, DetailView):
    model = ExchangeRate
    template_name = "finance/exchange_rate_detail.html"
    context_object_name = "rate"

    def get_queryset(self):
        return ExchangeRate.objects.filter(user=self.request.user)


class ExchangeRateCreateView(LoginRequiredMixin, CreateView):
    model = ExchangeRate
    form_class = ExchangeRateForm
    template_name = "finance/exchange_rate_create.html"
    success_url = reverse_lazy("finance:rate_list")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def form_valid(self, form):
        messages.success(self.request, "Курсы валют успешно добавлены.")
        return super().form_valid(form)


class ExchangeRateDeleteView(LoginRequiredMixin, DeleteView):
    model = ExchangeRate
    success_url = reverse_lazy("finance:rate_list")

    def get_queryset(self):
        return ExchangeRate.objects.filter(user=self.request.user)

    def form_valid(self, form):
        try:
            response = super().form_valid(form)
        except ProtectedError:
            messages.error(self.request, "Курс используется в поставках.")
            return redirect("finance:rate_list")
        messages.success(self.request, "Курс валют удален.")
        return response


class CalculationResultListView(LoginRequiredMixin, ListView):
    model = CalculationResult
    template_name = "finance/calculation_result_list.html"
    context_object_name = "results"
    paginate_by = 20

    def get_queryset(self):
        return (
            CalculationResult.objects.filter(shipment__user=self.request.user)
            .select_related("shipment", "exchange_rate")
            .order_by("-created_at")
        )


class CalculationResultDetailView(LoginRequiredMixin, DetailView):
    model = CalculationResult
    template_name = "finance/calculation_result_detail.html"
    context_object_name = "result"

    def get_queryset(self):
        return (
            CalculationResult.objects.filter(shipment__user=self.request.user)
            .select_related("shipment", "exchange_rate")
            .prefetch_related("client_results__client", "client_results__item_results__item")
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["client_results"] = (
            self.object.client_results
            .select_related("client")
            .prefetch_related("item_results__item")
            .annotate(total_weight=Sum("item_results__item__weight", default=0))
        )

        return context


class CalculationResultDeleteView(LoginRequiredMixin, DeleteView):
    model = CalculationResult
    template_name = "universal_form.html"
    success_url = reverse_lazy("finance:calculations_list")

    def get_queryset(self):
        return CalculationResult.objects.filter(
            shipment__user=self.request.user,
        )

    def form_valid(self, form):
        if self.object.is_actual:
            messages.error(
                self.request,
                "Актуальный результат расчёта удалить нельзя.",
            )
            return redirect("finance:calculations_list")

        messages.success(
            self.request,
            "Результат расчёта удалён.",
        )
        return super().form_valid(form)

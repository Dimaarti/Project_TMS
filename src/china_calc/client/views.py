from decimal import Decimal

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView

from china_calc.client.forms import ClientForm
from china_calc.client.models import Client
from china_calc.finance.models import ClientCalculationResult, ClientPayment
from china_calc.finance.services.client_balance_service import ClientBalanceService


class ClientListView(LoginRequiredMixin, ListView):
    model = Client
    template_name = "client/client_list.html"
    context_object_name = "clients"

    def get_queryset(self):
        return Client.objects.filter(user=self.request.user).order_by("full_name")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        clients = list(context["clients"])

        client_results = (
            ClientCalculationResult.objects.filter(
                client__in=clients,
                calculation_result__is_actual=True,
                calculation_result__shipment__user=self.request.user,
            )
            .select_related(
                "client", "calculation_result", "calculation_result__shipment"
            )
            .order_by("client_id", "-calculation_result__created_at")
        )

        payment_totals = {
            (row["client_id"], row["shipment_id"], row["currency"]): row["total"]
            for row in (
                ClientPayment.objects.filter(
                    client__in=clients,
                    shipment__user=self.request.user,
                )
                .values("client_id", "shipment_id", "currency")
                .annotate(total=Sum("amount"))
            )
        }

        balances_by_client = {client.pk: [] for client in clients}

        for client_result in client_results:
            shipment = client_result.calculation_result.shipment
            paid_amount = payment_totals.get(
                (
                    client_result.client_id,
                    shipment.pk,
                    client_result.calculation_result.final_currency,
                ),
                Decimal(0),
            )
            balance = ClientBalanceService.build(
                total_amount=client_result.client_price_cost, paid_amount=paid_amount
            )

            client_result.total_amount = balance["total_amount"]
            client_result.paid_amount = balance["paid_amount"]
            client_result.debt_amount = balance["debt_amount"]
            client_result.overpayment_amount = balance["overpayment_amount"]

            balances_by_client[client_result.client_id].append(client_result)
        for client in clients:
            client.payment_results = balances_by_client[client.pk]
        return context


class ClientCreateView(LoginRequiredMixin, CreateView):
    model = Client
    form_class = ClientForm
    template_name = "client/client_create.html"
    success_url = reverse_lazy("client:list")

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, "Клиент создан")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Новый клиент"
        context["submit_text"] = "Создать"
        return context


class ClientUpdateView(LoginRequiredMixin, UpdateView):
    model = Client
    form_class = ClientForm
    template_name = "client/client_create.html"

    def get_queryset(self):
        return Client.objects.filter(user=self.request.user)

    def form_valid(self, form):
        messages.success(self.request, "Данные клиента обновлены")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Редактирование клиента"
        context["submit_text"] = "Сохранить"
        return context

    def get_success_url(self):
        return reverse_lazy("client:list")

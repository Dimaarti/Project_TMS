from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.generic import CreateView, DeleteView, UpdateView

from china_calc.shipment.forms import ShipmentExpenseForm
from china_calc.shipment.models import Shipment, ShipmentExpense


class ShipmentExpenseCreateView(LoginRequiredMixin, CreateView):
    model = ShipmentExpense
    form_class = ShipmentExpenseForm
    template_name = "expenses/expense_create.html"

    def dispatch(self, request, *args, **kwargs):
        self.shipment = get_object_or_404(
            Shipment,
            pk=kwargs["shipment_pk"],
            user=request.user,
        )

        return super().dispatch(
            request,
            *args,
            **kwargs,
        )

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["shipment"] = self.shipment
        return kwargs

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.instance.shipment = self.shipment
        return form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Новый расход"
        context["shipment"] = self.shipment
        context["cancel_url"] = reverse(
            "shipment:detail", kwargs={"pk": self.shipment.pk}
        )
        return context

    def form_valid(self, form):
        form.instance.shipment = self.shipment

        response = super().form_valid(form)
        self.shipment.invalidate_calculations()

        messages.success(
            self.request,
            "Расход добавлен",
        )

        return response

    def get_success_url(self):
        return reverse(
            "shipment:detail",
            kwargs={"pk": self.shipment.pk},
        )


class ShipmentExpenseUpdateView(LoginRequiredMixin, UpdateView):
    model = ShipmentExpense
    form_class = ShipmentExpenseForm
    template_name = "expenses/expense_create.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Редактирование расхода"
        context["cancel_url"] = reverse(
            "shipment:detail",
            kwargs={"pk": self.object.shipment_id},
        )
        return context

    def get_queryset(self):
        return ShipmentExpense.objects.filter(
            shipment__user=self.request.user
        ).select_related(
            "shipment",
            "item",
        )

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["shipment"] = self.object.shipment

        return kwargs

    def get_success_url(self):
        messages.success(
            self.request,
            "Расход обновлён",
        )

        return reverse(
            "shipment:detail",
            kwargs={"pk": self.object.shipment_id},
        )

    def form_valid(self, form):
        response = super().form_valid(form)
        self.object.shipment.invalidate_calculations()
        return response


class ShipmentExpenseDeleteView(LoginRequiredMixin, DeleteView):
    model = ShipmentExpense
    template_name = "universal_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Удаление расхода"
        context["delete_mode"] = True
        context["cancel_url"] = reverse(
            "shipment:detail",
            kwargs={"pk": self.object.shipment_id},
        )
        return context

    def get_success_url(self):
        shipment_id = self.object.shipment_id
        self.object.shipment.invalidate_calculations()

        messages.success(
            self.request,
            "Расход удалён",
        )

        return reverse(
            "shipment:detail",
            kwargs={"pk": shipment_id},
        )

    def get_queryset(self):
        return ShipmentExpense.objects.filter(
            shipment__user=self.request.user
        ).select_related("shipment")

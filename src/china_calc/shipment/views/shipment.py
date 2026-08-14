from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.db.models import Count
from django.urls import reverse
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from china_calc.shipment.forms import ShipmentForm
from china_calc.shipment.models import Shipment


class ShipmentListView(LoginRequiredMixin, ListView):
    model = Shipment
    template_name = "shipment/shipment_list.html"
    context_object_name = "shipments"
    paginate_by = 5

    def get_queryset(self):
        return (Shipment.objects.filter(user=self.request.user)
                .select_related("route", "exchange_rate")
                .order_by("pk")
        )


class ShipmentDetailView(LoginRequiredMixin, DetailView):
    model = Shipment
    template_name = "shipment/shipment_detail.html"
    context_object_name = "shipment"

    def get_queryset(self):
        return (
            Shipment.objects.filter(user=self.request.user)
                .select_related("route", "exchange_rate")
                .prefetch_related("expenses", "calculation_results")
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        items_queryset = (
            self.object.items
            .select_related("client")
            .order_by("pk")
        )

        paginator = Paginator(
            items_queryset,
            15,
        )

        items_page = paginator.get_page(
            self.request.GET.get("items_page")
        )

        context["items"] = items_page.object_list
        context["items_page"] = items_page

        context["actual_result"] = (
            self.object.calculation_results
            .filter(is_actual=True)
            .order_by("-created_at")
            .first()
        )

        return context


class ShipmentCreateView(LoginRequiredMixin, CreateView):
    model = Shipment
    form_class = ShipmentForm
    template_name = "shipment/shipment_create.html"

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Новая поставка"
        context["cancel_url"] = reverse("shipment:list")
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        messages.success(
            self.request,
            "Поставка создана.",
        )

        return reverse(
            "shipment:detail",
            kwargs={"pk": self.object.pk},
        )


class ShipmentUpdateView(LoginRequiredMixin, UpdateView):
    model = Shipment
    form_class = ShipmentForm
    template_name = "shipment/shipment_create.html"
    context_object_name = "shipment"

    def get_queryset(self):
        return Shipment.objects.filter(user=self.request.user)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Редактирование поставки"
        context["cancel_url"] = reverse("shipment:detail", kwargs={"pk": self.object.pk})
        return context

    def get_success_url(self):
        messages.success(self.request, "Поставка обновлена")
        return reverse("shipment:detail", kwargs={"pk": self.object.pk})

    def form_valid(self, form):
        form.instance.user = self.request.user
        response = super().form_valid(form)
        self.object.invalidate_calculations()
        return response


class ShipmentDeleteView(LoginRequiredMixin, DeleteView):
    model = Shipment
    template_name = "universal_form.html"

    def get_queryset(self):
        return (
            Shipment.objects.filter(user=self.request.user)
            .select_related("route", "exchange_rate")
            .annotate(items_count=Count("items"))
            .order_by("-created_at")

        )


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Удаление поставки"
        context["delete_mode"] = True
        context["cancel_url"] = reverse("shipment:detail", kwargs={"pk": self.object.pk})
        return context

    def get_success_url(self):
        messages.success(self.request, "Поставка успешно удалена")
        return reverse("shipment:list")


from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import FileResponse, HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.utils.text import slugify
from django.views import View

from china_calc.client.models import Client
from china_calc.reports.services.report_item_list_services import (
    ShipmentPackingListServices,
)
from china_calc.reports.services.report_services import ShipmentReportServices
from china_calc.shipment.models import Shipment


class ShipmentReportView(LoginRequiredMixin, View):
    def get(self, request, shipment_pk, client_pk):
        shipment = get_object_or_404(
            Shipment.objects.select_related("exchange_rate"),
            pk=shipment_pk,
            user=request.user,
        )

        client = get_object_or_404(
            Client.objects.filter(
                user=request.user,
                shipment_items__shipment=shipment,
            ).distinct(),
            pk=client_pk,
        )

        try:
            report_file = ShipmentReportServices(
                shipment=shipment,
                client=client,
            ).build()

        except ValueError as error:
            messages.error(request, str(error))

            calculation_result = (
                shipment.calculation_results.filter(is_actual=True)
                .order_by("-created_at")
                .first()
            )

            if calculation_result is not None:
                return redirect(
                    "finance:calculations_detail",
                    pk=calculation_result.pk,
                )
            return redirect("shipment:detail", pk=shipment.pk)

        client_name = slugify(client.full_name, allow_unicode=True)
        filename = f"Отчет_поставки_{shipment.pk}_клиент_{client_name}.xlsx"

        return FileResponse(
            report_file,
            as_attachment=True,
            filename=filename,
            content_type=(
                "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            ),
        )


class ShipmentPackingListView(LoginRequiredMixin, View):
    def get(self, request, pk):
        shipment = get_object_or_404(Shipment, pk=pk, user=request.user)

        try:
            buffer = ShipmentPackingListServices(shipment).build()
        except ValueError as e:
            return HttpResponse(str(e), status=400)

        response = HttpResponse(
            buffer.getvalue(),
            content_type=(
                "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            ),
        )
        response["Content-Disposition"] = (
            f'attachment; filename="packing_list_{shipment.number}.xlsx"'
        )
        return response

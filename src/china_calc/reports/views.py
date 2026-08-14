from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import FileResponse
from django.shortcuts import get_object_or_404, redirect
from django.views import View

from china_calc.client.models import Client
from china_calc.reports.services.report_services import ShipmentReportServices
from china_calc.shipment.models import Shipment


class ShipmentReportView(LoginRequiredMixin, View):
    def get(self, request, shipment_pk, client_pk):
        shipment = get_object_or_404(
            Shipment.objects.select_related(
                "route", "exchange_rate"
            ),
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

        except ValueError:
            messages.error(request, "Ошибка")
            return redirect("finance:calculations_detail",
                            pk=shipment.calculation_results
                            .filter(is_actual=True).first()
                            )

        filename = (f"shipment_report_{shipment.pk}"
                    f"client_{client.full_name}.xlsx")

        return FileResponse(
            report_file, as_attachment=True, filename=filename, content_type="text/xlsx"
        )

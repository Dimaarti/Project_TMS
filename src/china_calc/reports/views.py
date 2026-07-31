from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import FileResponse
from django.shortcuts import get_object_or_404
from django.views import View

from china_calc.reports.services.report_services import ShipmentReportServices
from china_calc.shipment.models import Shipment


class ShipmentReportView(LoginRequiredMixin, View):
    def get(self, request, pk):
        shipment = get_object_or_404(
            Shipment.objects.select_related(
                "route", "exchange_rate", "calculation_result"
            ).prefetch_related("item__product", "item__client"),
            pk=pk,
            user=request.user,
        )

        report_service = ShipmentReportServices(shipment)
        report_file = report_service.build()
        filename = f"shipment_report_{pk}.xlsx"
        return FileResponse(
            report_file, as_attachment=True, filename=filename, content_type="text/xlsx"
        )

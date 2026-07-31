from django.urls import path

from china_calc.reports.views import ShipmentReportView

app_name = "reports"

urlpatterns = [
    path("<int:pk>/reports/", ShipmentReportView.as_view(), name="shipment_reports")
]

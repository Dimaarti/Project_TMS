from django.urls import path

from china_calc.reports.views import ShipmentPackingListView, ShipmentReportView

app_name = "reports"

urlpatterns = [
    path(
        "<int:shipment_pk>/clients/<int:client_pk>/report/",
        ShipmentReportView.as_view(),
        name="shipment_report",
    ),
    path(
        "<int:pk>/packing-list/",
        ShipmentPackingListView.as_view(),
        name="packing_list",
    ),
]

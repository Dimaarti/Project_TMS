from django.urls import path

from china_calc.finance.views import ShipmentCalculateView
from china_calc.shipment.views import (
    ItemCreateView,
    ShipmentCreateView,
    ShipmentDeleteView,
    ShipmentDetailView,
    ShipmentListView,
    ShipmentUpdateView,
)

app_name = "shipment"

urlpatterns = [
    path("", ShipmentListView.as_view(), name="list"),
    path("create/", ShipmentCreateView.as_view(), name="create"),
    path("<int:pk>/update/", ShipmentUpdateView.as_view(), name="update"),
    path("<int:pk>/delete/", ShipmentDeleteView.as_view(), name="delete"),
    path("<int:pk>/", ShipmentDetailView.as_view(), name="detail"),
    path("<int:pk>/calculate/", ShipmentCalculateView.as_view(), name="calculate"),
    path("<int:pk>/create/", ItemCreateView.as_view(), name="item_create"),
]

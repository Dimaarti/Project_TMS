from django.urls import path

from china_calc.finance.views import ShipmentCalculateView
from china_calc.shipment.views.shipment import (
    ShipmentCreateView,
    ShipmentDeleteView,
    ShipmentDetailView,
    ShipmentListView,
    ShipmentUpdateView,
)
from china_calc.shipment.views.shipment_expense import (
    ShipmentExpenseCreateView,
    ShipmentExpenseDeleteView,
    ShipmentExpenseUpdateView,
)
from china_calc.shipment.views.shipment_item import (
    ShipmentItemCreateView,
    ShipmentItemDeleteView,
    ShipmentItemUpdateView,
)

app_name = "shipment"

urlpatterns = [
    path("", ShipmentListView.as_view(), name="list"),
    path("create/", ShipmentCreateView.as_view(), name="create"),
    path("<int:pk>/update/", ShipmentUpdateView.as_view(), name="update"),
    path("<int:pk>/delete/", ShipmentDeleteView.as_view(), name="delete"),
    path("<int:pk>/", ShipmentDetailView.as_view(), name="detail"),
    path("<int:pk>/calculate/", ShipmentCalculateView.as_view(), name="calculate"),
    path(
        "<int:shipment_pk>/items/create/",
        ShipmentItemCreateView.as_view(),
        name="item_create",
    ),
    path("items/<int:pk>/update/", ShipmentItemUpdateView.as_view(), name="item_update"),
    path("items/<int:pk>/delete/", ShipmentItemDeleteView.as_view(), name="item_delete"),
    path(
        "expenses/<int:shipment_pk>/create/",
        ShipmentExpenseCreateView.as_view(),
        name="expense_create",
    ),
    path(
        "expenses/<int:pk>/update/",
        ShipmentExpenseUpdateView.as_view(),
        name="expense_update",
    ),
    path(
        "expenses/<int:pk>/delete/",
        ShipmentExpenseDeleteView.as_view(),
        name="expense_delete",
    ),
]

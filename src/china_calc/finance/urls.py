from django.urls import path

from china_calc.finance.views import (
    CalculationResultDeleteView,
    CalculationResultDetailView,
    CalculationResultListView,
    ClientPaymentCreateView,
    ExchangeRateCreateView,
    ExchangeRateDeleteView,
    ExchangeRateDetailView,
    ExchangeRateListView,
)

app_name = "finance"

urlpatterns = [
    path("", ExchangeRateListView.as_view(), name="rate_list"),
    path("rate/<int:pk>", ExchangeRateDetailView.as_view(), name="rate_detail"),
    path("rate/create/", ExchangeRateCreateView.as_view(), name="rate_create"),
    path("rate/<int:pk>/delete/", ExchangeRateDeleteView.as_view(), name="rate_delete"),
    path(
        "calculations/",
        CalculationResultListView.as_view(),
        name="calculations_list",
    ),
    path(
        "calculations/<int:pk>/",
        CalculationResultDetailView.as_view(),
        name="calculations_detail",
    ),
    path(
        "calculations/<int:pk>/delete/",
        CalculationResultDeleteView.as_view(),
        name="calculations_delete",
    ),
    path(
        "shipments/<int:shipment_pk>/clients/<int:client_pk>/payments/create/",
        ClientPaymentCreateView.as_view(),
        name="client_payment_create",
    ),
]

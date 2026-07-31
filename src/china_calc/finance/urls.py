from django.urls import path

from china_calc.finance.views import (
    ExchangeRateCreateView,
    ExchangeRateDeleteView,
    ExchangeRateDetailView,
    ExchangeRateListView,
)

app_name = "finance"

urlpatterns = [
    path("", ExchangeRateListView.as_view(), name="list"),
    path("create/", ExchangeRateCreateView.as_view(), name="create"),
    path("<int:pk>/", ExchangeRateDetailView.as_view(), name="detail"),
    path("<int:pk>/delete/", ExchangeRateDeleteView.as_view(), name="delete"),
]

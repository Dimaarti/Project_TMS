from django.urls import include, path

urlpatterns = [
    path("account/", include("china_calc.account.urls")),
    path("shipment/", include("china_calc.shipment.urls")),
    path("client/", include("china_calc.client.urls")),
    path("finance/", include("china_calc.finance.urls")),
    path("reports/", include("china_calc.reports.urls")),
]

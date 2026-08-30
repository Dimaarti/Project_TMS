from django.urls import path

from china_calc.client.views import (
    ClientCreateView,
    ClientDeleteView,
    ClientListView,
    ClientUpdateView,
)

app_name = "client"

urlpatterns = [
    path("", ClientListView.as_view(), name="list"),
    path("create/", ClientCreateView.as_view(), name="create"),
    path("<int:pk>/update/", ClientUpdateView.as_view(), name="update"),
    path("<int:pk>/delete/", ClientDeleteView.as_view(), name="delete"),
]

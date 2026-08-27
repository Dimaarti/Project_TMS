from django.urls import path

from china_calc.account.views import Login, Logout, RegistrationView

app_name = "account"

urlpatterns = [
    path("login/", Login.as_view(), name="login"),
    path("register/", RegistrationView.as_view(), name="register"),
    path("logout/", Logout.as_view(), name="logout"),
]

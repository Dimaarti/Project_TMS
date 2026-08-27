from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView

from china_calc.account.forms import UserRegistrationForm
from china_calc.account.models import User


class Login(LoginView):
    template_name = "account/login.html"


class Logout(LogoutView):
    next_page = "account:login"


class RegistrationView(CreateView):
    model = User
    form_class = UserRegistrationForm
    template_name = "account/registration.html"
    success_url = reverse_lazy("shipment:list")

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("shipment:list")

        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)

        return response

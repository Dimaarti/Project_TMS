from django.contrib.auth.views import LoginView, LogoutView


class Login(LoginView):
    template_name = "account/login.html"



class Logout(LogoutView):
    next_page = "account:login"

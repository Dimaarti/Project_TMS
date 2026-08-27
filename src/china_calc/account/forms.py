from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from china_calc.account.models import User


class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("first_name", "last_name", "email")

        labels = {"first_name": "Имя", "last_name": "Фамилия", "email": "Email"}

    def clean_email(self):
        email = self.cleaned_data["email"].strip().lower()
        if User.objects.filter(email__iexact=email).exists():
            raise ValidationError(
                "Пользователь с такой электронной почтой уже существует"
            )

        return email

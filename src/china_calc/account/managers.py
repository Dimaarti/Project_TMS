from django.contrib.auth.base_user import BaseUserManager

from django.contrib.auth.hashers import make_password


class UserManager(BaseUserManager):
    def _create_user(self, email, password, **kwargs):
        user = self.model(email=email, **kwargs)
        user.password = make_password(password)
        user.save()
        return user

    def create_user(self, email, password):
        return self._create_user(email, password)

    def create_superuser(self, email, password):
        kwargs = {
            'is_superuser': True,
            'is_staff': True,
        }
        return self._create_user(email, password, **kwargs)
from unittest import TestCase

from china_calc.account.models import User


class TestClientView(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="test@test.com", password="test")

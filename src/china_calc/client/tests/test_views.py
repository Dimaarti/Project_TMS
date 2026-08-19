from decimal import Decimal
from unittest import TestCase

from china_calc.account.models import User
from china_calc.client.models import Client


class TestClientView(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='test@test.com',
            password='test'
        )
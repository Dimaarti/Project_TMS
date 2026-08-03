from django.test import Client, TestCase
from django.urls import reverse

from china_calc.account.models import User


class TestClientView(TestCase):
    def setUp(self):
        self.client = Client()
        test_user_email = "test@test.com"
        test_user_password = "1111"
        self.user = User.objects.create_user(
            email=test_user_email, password=test_user_password
        )
        self.client.force_login(self.user)

    def test_list(self):
        response = self.client.get(reverse("client:list"))

        self.assertEqual(response.status_code, 200)

    def test_create(self):
        response = self.client.post(
            reverse("client:create"),
            data={
                "full_name": "Дима",
                "phone": 111,
                "address": "Минск",
                "buyer_commission_percent": 5,
            },
        )

        self.assertRedirects(response, reverse("client:list"))

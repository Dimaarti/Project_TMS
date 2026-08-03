import datetime

from django.test import Client, TestCase
from django.urls import reverse

from china_calc.account.models import User
from china_calc.finance.models.exchange_rate import ExchangeRate


class TestExchangeRateView(TestCase):
    def setUp(self):
        self.client = Client()
        test_user_email = "test@test.com"
        test_user_password = "2222"
        self.user = User.objects.create_user(
            email=test_user_email, password=test_user_password
        )
        self.client.force_login(self.user)

        self.exchange_rate = ExchangeRate.objects.create(
            date=datetime.date.today(),
            cny_to_byn=0.4500,
            cny_to_byn_client=0.5000,
            cny_to_rub=12.0000,
            cny_to_rub_client=13.0000,
            usd_to_byn=3.2000,
            usd_to_byn_client=3.3000,
            usd_to_rub=90.0000,
            usd_to_rub_client=91.0000,
            rub_to_byn=0.0300,
            rub_to_byn_client=0.0500,
        )

    def test_list(self):
        response = self.client.get(reverse("finance:list"))

        self.assertEqual(response.status_code, 200)

    def test_detail(self):
        response = self.client.get(
            reverse("finance:detail", kwargs={"pk": self.exchange_rate.pk})
        )

        self.assertEqual(response.status_code, 200)

    def test_create(self):
        response = self.client.post(
            reverse("finance:create"),
            data={
                "date": datetime.date.today(),
                "cny_to_byn": 0.4500,
                "cny_to_byn_client": 0.5000,
                "cny_to_rub": 12.0000,
                "cny_to_rub_client": 13.0000,
                "usd_to_byn": 3.2000,
                "usd_to_byn_client": 3.3000,
                "usd_to_rub": 90.0000,
                "usd_to_rub_client": 91.0000,
                "rub_to_byn": 0.0300,
                "rub_to_byn_client": 0.0500,
            },
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(ExchangeRate.objects.count(), 2)

    def test_delete(self):
        response = self.client.post(
            reverse("finance:delete", kwargs={"pk": self.exchange_rate.pk})
        )

        self.assertEqual(response.status_code, 302)
        self.assertFalse(ExchangeRate.objects.filter(pk=self.exchange_rate.pk).exists())

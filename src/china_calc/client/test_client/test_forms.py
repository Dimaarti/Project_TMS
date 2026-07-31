from django.test import Client, TestCase

from china_calc.account.models import User
from china_calc.client.forms import ClientForm


class TestClientForms(TestCase):
    def setUp(self):
        self.client = Client()
        test_user_email = "test@test.com"
        test_user_password = "1111"
        self.user = User.objects.create_user(
            email=test_user_email, password=test_user_password
        )
        self.client.force_login(self.user)

        self.data = {
            "user": self.user.pk,
            "full_name": "test full name",
            "phone": "000",
            "address": "Minsk",
            "buyer_commission_percent": 5.00
        }

    def test_form_is_valid(self):
        form = ClientForm(data=self.data)
        self.assertTrue(form.is_valid())

    def test_full_name_is_required(self):
        data = self.data.copy()
        data["full_name"] = ""
        form = ClientForm(data=data)

        self.assertFalse(form.is_valid())

    def test_form_save(self):
        form = ClientForm(data=self.data)

        self.assertTrue(form.is_valid())

        client = form.save()

        self.assertEqual(client.user, self.user)
        self.assertEqual(client.full_name, "test full name")
        self.assertEqual(client.buyer_commission_percent, 5.00)

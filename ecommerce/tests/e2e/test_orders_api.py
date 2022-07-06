from statistics import mode
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APITestCase

from knox.models import AuthToken

from ecommerce import models

User = get_user_model()

class OrderApiTests(APITestCase):

    def setUp(self):
        self.test_user = User.objects.create(
            name="user", email="user@test.com", is_active=True
        )

    def set_credentials(self, user, create_token: bool = False):
        instance, token = AuthToken.objects.create(user=user)
        print("token")
        print(token)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)
        self.client.force_login(user=user)

    # TODO(alex): mock third party call
    def test_create_happy_path(self):
        self.set_credentials(self.test_user)
        url = reverse("ecommerce:orders-list")
        response = self.client.post(url, {})
        self.assertEqual(response.status_code, 201)

    # TODO(alex): mock third party call
    def test_add_order_line_happy_path(self):
        self.set_credentials(self.test_user)
        order = models.Order.objects.create(
            user=self.test_user,
        )
        url = reverse("ecommerce:orders-add-order-line", args=[str(order.id),])
        product = models.Product.objects.create(
            name="keyboard",
            price=800,
            stock=5
        )
        data = {
            "product": str(product.id),
            "quantity": 2
        }
        response = self.client.patch(url, data, format="json")
        response_data = response.json()["data"]
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data["total"], 1600.0)
        self.assertTrue(len(response_data["order_lines"]))
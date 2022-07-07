from mock import patch

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

    def _set_credentials(self, user, create_token: bool = False):
        instance, token = AuthToken.objects.create(user=user)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)
        self.client.force_login(user=user)


    @patch(
        "ecommerce.serializers.OrderModelSerializer.get_total_usd",
        return_value=100
    )
    def test_create_happy_path(self, _):
        self._set_credentials(self.test_user)
        url = reverse("ecommerce:orders-list")
        response = self.client.post(url, {})
        self.assertEqual(response.status_code, 201)
        expected_keys = ["id", "order_lines", "total", "total_usd", "date_time", "user"]
        received_keys = list(response.json()["data"].keys())
        self.assertListEqual(expected_keys, received_keys)


    @patch(
        "ecommerce.serializers.OrderModelSerializer.get_total_usd",
        return_value=100
    )
    def test_add_order_line_happy_path(self, _):
        self._set_credentials(self.test_user)
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


    @patch(
        "ecommerce.serializers.OrderModelSerializer.get_total_usd",
        return_value=100
    )
    def test_order_line_update_quantity_then_product_stock_is_updated(self, _):
        self._set_credentials(self.test_user)
        order = models.Order.objects.create(
            user=self.test_user,
        )
        url = reverse("ecommerce:orders-add-order-line", args=[str(order.id),])
        product = models.Product.objects.create(
            name="keyboard",
            price=800,
            stock=8
        )
        data = {
            "product": str(product.id),
            "quantity": 5
        }
        response = self.client.patch(url, data, format="json")
        response_data = response.json()["data"]
        product.refresh_from_db()
        self.assertEqual(product.stock, 3)
        self.assertTrue(len(response_data["order_lines"]), 1)
        url = reverse("ecommerce:orders-update-order-line-quantity", args=[str(order.id),])
        # remove 2 items
        data["quantity"] = 3
        response = self.client.patch(url, data, format="json")
        self.assertTrue(len(response_data["order_lines"]), 0)
        product.refresh_from_db()
        self.assertEqual(product.stock, 5)



    
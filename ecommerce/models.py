from uuid import uuid4
import decimal

from django.db import models
from django.db.models import Sum
from django.contrib.auth import get_user_model

from ecommerce.layer_service.rate_exchange import RateExchange

User = get_user_model()

class Product(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid4, editable=False
    )
    name = models.CharField(max_length=64)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)


class Order(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid4, editable=False
    )
    user = models.ForeignKey(to=User, on_delete=models.SET_NULL, null=True)
    date_time = models.DateTimeField(auto_now_add=True)

    def get_total(self) -> decimal.Decimal:
        total = decimal.Decimal()
        for line in self.orders_detail.all():
            total += line.product.price * line.quantity

        return total

    def get_total_usd(self) -> decimal.Decimal:
        total = decimal.Decimal()
        for line in self.orders_detail.all():
            total += line.product.price * line.quantity

        rate = RateExchange.fetch_rate_usd_blue()
        return total * rate

class OrderDetail(models.Model):
    order = models.ForeignKey(
        to=Order, on_delete=models.CASCADE, related_name="orders_detail"
    )
    product = models.ForeignKey(
        to=Product, on_delete=models.SET_NULL, related_name="orders_detail", null=True
    )
    quantity = models.PositiveIntegerField()

    class Meta:
        unique_together = ("order", "product")


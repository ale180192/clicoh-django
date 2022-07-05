from itertools import product
from uuid import uuid4

from django.db import models


class Product(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid4, editable=False
    )
    name = models.CharField(max_length=64)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    stock = models.PositiveIntegerField()


class Order(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid4, editable=False
    )
    date_time = models.DateTimeField(auto_now_add=True)

class OrderDetail(models.Model):
    order = models.ForeignKey(
        to=Order, on_delete=models.CASCADE, related_name="orders_detail"
    )
    product = models.ForeignKey(
        to=Product, on_delete=models.SET_NULL, related_name="orders_detail", null=True
    )
    quantity = models.PositiveIntegerField()


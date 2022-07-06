from dataclasses import field
from rest_framework import serializers

from . import models

class ProductModelSerializer(serializers.ModelSerializer):
    """
    It's no possible update the field stock with this serializer.
    """
    class Meta:
        model = models.Product
        fields = "__all__"
        extra_kwargs = {
            "stock": {"read_only": True},
        }

class ProductUpdateStockModelSerializer(serializers.ModelSerializer):
    """
    Only the stock field is possible to update.
    """

    class Meta:
        model = models.Product
        fields = "__all__"
        extra_kwargs = {
            "name": {"read_only": True},
            "price": {"read_only": True},
        }

       
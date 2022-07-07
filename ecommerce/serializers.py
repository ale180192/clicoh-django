from rest_framework import serializers
from rest_framework import status

from . import models
from app.api_exceptions import CustomAPIException
from app.api_error_codes import ErrorCode

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



class OrderDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.OrderDetail
        fields = "__all__"

    def validate(self, data):
        product = data.get("product")
        if product.stock < data.get("quantity"):
            msg = f"it's only {product.stock} items availables."
            raise CustomAPIException(
                error=ErrorCode.OUT_OF_STOCK,
                status_code=status.HTTP_400_BAD_REQUEST,
                error_detail=msg
            )

        return data

class OrderModelSerializer(serializers.ModelSerializer):
    order_lines = OrderDetailSerializer(
        many=True, source="orders_detail", read_only=True
    )
    total = serializers.SerializerMethodField()
    total_usd = serializers.SerializerMethodField()

    class Meta:
        model = models.Order
        fields = "__all__"

    def validate(self, data: str) -> dict:
        data["user"] = self.context["request"].user
        return data


    def get_total(self, instance: models.Order) -> float:
        return instance.get_total()

    def get_total_usd(self, instance: models.Order) -> float:
        return instance.get_total_usd()


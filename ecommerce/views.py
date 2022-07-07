import logging

from django.db.models import F
from rest_framework.decorators import action
from rest_framework.permissions import (
    IsAuthenticated
)
from rest_framework import status

from knox.auth import TokenAuthentication
from app.api_error_codes import ErrorCode
from app.api_exceptions import CustomAPIException

from app.base_views import BaseModelViewSet
from app import api_utils
from . import models
from . import serializers

logger = logging.getLogger(__name__)

class ProductsViewSet(BaseModelViewSet):
    """
        post:
        Create a single Product record on DB with data passed on request.
        get:
        Returns all Products records.
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, ]
    queryset = models.Product.objects.all()
    serializer_class = serializers.ProductModelSerializer

    @action(detail=True, methods=['patch'], url_path="update_stock")
    def update_stock(self, request, pk):
        product = self.get_object()
        ser = serializers.ProductUpdateStockModelSerializer(product, data=request.data, partial=True)
        ser.is_valid(raise_exception=True)
        ser.save()
        return api_utils.response_success(data=ser.data)


class OrdersViewSet(BaseModelViewSet):
    """
        post:
        Create a single Order record on DB with data passed on request.
        get:
        Returns all Orders records.
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, ]
    queryset = models.Order.objects.all()
    serializer_class = serializers.OrderModelSerializer
        
    @action(detail=True, methods=['patch'], url_path="add_order_line")
    def add_order_line(self, request, pk):
        data = request.data
        data["order"] = pk
        ser = serializers.OrderDetailSerializer(data=data)
        ser.is_valid(raise_exception=True)
        order_line = ser.save()
        models.Product.objects \
            .filter(pk=order_line.product.id) \
            .update(stock=F("stock") - order_line.quantity)
        order = self.get_object()
        serializer_order = serializers.OrderModelSerializer(order)
        return api_utils.response_success(data=serializer_order.data)

    @action(detail=True, methods=['patch'], url_path="remove_order_line")
    def remove_order_line(self, request, pk):
        order = self.get_object()
        data = request.data
        product = models.Product.objects.get(pk=data.get("product"))
        order_line = models.OrderDetail.objects.get(product=product, order=order)
        order_line.delete()
        models.Product.objects \
            .filter(pk=order_line.product.id) \
            .update(stock=F("stock") + order_line.quantity)
        serializer_order = serializers.OrderModelSerializer(order)
        return api_utils.response_success(data=serializer_order.data)

    @action(detail=True, methods=['patch'], url_path="update_order_line_quantity")
    def update_order_line_quantity(self, request, pk):
        data = request.data
        data["order"] = pk
        order = self.get_object()
        product = models.Product.objects.get(pk=data.get("product"))
        order_line = models.OrderDetail.objects.get(product=product, order=order)
        diff = order_line.quantity - data["quantity"]
        if diff > 0:
            is_added = False
        else:
            is_added = True

        if is_added:
            if product.stock >= diff:
                models.Product.objects \
                    .filter(pk=order_line.product.id) \
                    .update(stock=F("stock") - diff)
                order_line.quantity += diff
                order_line.save()
            else:
                msg = f"it's only {product.stock} items availables."
                logger.error(msg)
                raise CustomAPIException(
                error=ErrorCode.OUT_OF_STOCK,
                status_code=status.HTTP_400_BAD_REQUEST,
                error_detail=msg
            )
        else:
            models.Product.objects \
                    .filter(pk=order_line.product.id) \
                    .update(stock=F("stock") + diff)
            order_line.quantity -= diff
            order_line.save()

        serializer_order = serializers.OrderModelSerializer(order)
        return api_utils.response_success(data=serializer_order.data)




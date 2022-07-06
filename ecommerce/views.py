from rest_framework.decorators import action
from rest_framework.permissions import (
    IsAuthenticated,
    IsAdminUser,
)

from knox.auth import TokenAuthentication

from app.base_views import BaseModelViewSet
from app import api_utils
from . import models
from . import serializers


class ProductsViewSet(BaseModelViewSet):
    """
        post:
        Create a single Product record on DB with data passed on request.
        get:
        Returns all Products records.
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminUser, IsAuthenticated]
    queryset = models.Product.objects.all()
    serializer_class = serializers.ProductModelSerializer

    @action(detail=True, methods=['patch'], url_path="update_stock")
    def update_stock(self, request, pk):
        product = self.get_object()
        ser = serializers.ProductUpdateStockModelSerializer(product, data=request.data, partial=True)
        ser.is_valid(raise_exception=True)
        ser.save()
        return api_utils.response_success(data=ser.data)
        




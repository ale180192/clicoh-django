from django.shortcuts import get_object_or_404
from django.http import Http404
from rest_framework.viewsets import ModelViewSet
from rest_framework import status

from app import api_utils
from app import api_exceptions
from app.api_error_codes import ErrorCode

class BaseModelViewSet(ModelViewSet):
    """
    Base class that override de response structure.
    """
    validation_handler = True

    def get_object(self):
        """
        Override method to be able to handle correctly the
        exception/error_code.
        """
        id = self.kwargs[self.lookup_field]
        queryset = self.filter_queryset(self.get_queryset())
        queryset = queryset.filter(id=id)
        try:
            obj = get_object_or_404(queryset)
        except Http404:
            raise api_exceptions.CustomAPIException(
                error=ErrorCode.NOT_FOUND,
                status_code=status.HTTP_404_NOT_FOUND,
            )

        self.check_object_permissions(self.request, obj)
        return obj

    def retrieve(self, request, *args, **kwargs):
        resp = super().retrieve(request, *args, **kwargs)
        return api_utils.response_success(
            resp.data, status=resp.status_code
        )

    def create(self, request, *args, **kwargs):
        resp = super().create(request, *args, **kwargs)
        return api_utils.response_success(
            resp.data, status=resp.status_code
        )

    def list(self, request, *args, **kwargs):
        resp = super().list(request, *args, **kwargs)
        return api_utils.response_success(
            resp.data, status=resp.status_code
        )

    def update(self, request, *args, **kwargs):
        resp = super().update(request, *args, **kwargs)
        return api_utils.response_success(
            resp.data, status=resp.status_code
        )

    def destroy(self, request, *args, **kwargs):
        resp = super().destroy(request, *args, **kwargs)
        return api_utils.response_success(
            resp.data, status=resp.status_code
        )
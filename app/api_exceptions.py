from rest_framework.exceptions import APIException


class CustomAPIException(APIException):
    """
    This exception is useful for we be able to handle the custom responses
    using serializers and we can raise custom exceptions, indicating the 
    status_code and the error(ErrorCode class).
    """

    def __init__(self, error, status_code, error_detail=None, errors=[]):
        self.error = error
        self.status_code = status_code
        self.error_detail = error_detail
        self.detail = self.error_detail if self.error_detail else self.error.value
        self.errors = errors

    def __str__(self):
        return f"{self.error} -> {self.detail}"

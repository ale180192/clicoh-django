from enum import Enum


class ErrorCode(Enum):
    """
    this class is used to return to the client an error with an 
    agreed format and it is possible to handle these events correctly
    """
    NOT_FOUND = "Not found"
    INVALID_CREDENTIALS = "You are not logged or your credentials are invalid."
    PEMISSION_FORBIDDEN = "Forbidden"
    BAD_REQUEST = "Bad request"
    OUT_OF_STOCK = "The stock of this product is not enough."
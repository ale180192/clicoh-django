from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):

    username = None
    name = models.CharField("name", max_length=50, default="user")
    email = models.EmailField("email address", unique=True)
    password_token = models.CharField("token", max_length=200, default="")
    updated_at = models.DateTimeField(null=True, auto_now=True)
    is_password_set = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email


"""app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path(", views.home, name="home")
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path(", Home.as_view(), name="home")
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path("blog/", include("blog.urls"))
"""
from django.urls import path, include


from knox import views as knox_views
from users.views import LoginView
from ecommerce.views import (
    ProductsViewSet,
    OrdersViewSet
)

from rest_framework.routers import SimpleRouter

router = SimpleRouter()
router.register(
    "api/ecommerce/v1/products", ProductsViewSet, basename="products"
)
# router.register(
#     "api/ecommerce/v1/orders", OrdersViewSet, basename="orders"
# )

urlpatterns = [
    path("login", LoginView.as_view(), name="knox_login"),
    path("logout", knox_views.LogoutView.as_view(), name="knox_logout"),
    path("logoutall", knox_views.LogoutAllView.as_view(), name="knox_logoutall"),
    path("api/ecommerce/v1/", include("ecommerce.urls", namespace="orders",))
]

urlpatterns += router.urls

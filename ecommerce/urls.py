from ecommerce.views import (
    ProductsViewSet,
    OrdersViewSet
)

from rest_framework.routers import SimpleRouter

router = SimpleRouter()

app_name = "ecommerce"
router.register(
    "orders", OrdersViewSet, basename="orders"
)
urlpatterns = router.urls

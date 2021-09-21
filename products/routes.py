from rest_framework import routers
from products.viewsets import ProductViewSet


router = routers.SimpleRouter()
router.register(r"products", ProductViewSet, basename="product")

urlpatterns = []
urlpatterns += router.urls

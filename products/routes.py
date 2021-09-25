from rest_framework import routers
from products.viewsets import ProductViewSet, ProductTypeViewSet


router = routers.SimpleRouter()
router.register(r"products", ProductViewSet, basename="product")
router.register(r"product-types", ProductTypeViewSet, basename="product-type")

urlpatterns = []
urlpatterns += router.urls

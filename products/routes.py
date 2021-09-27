from rest_framework import routers
from products.viewsets import ProductViewSet, ProductTypeViewSet


router = routers.SimpleRouter()
router.register(r"product-types", ProductTypeViewSet, basename="product-type")

urlpatterns = []
urlpatterns += router.urls

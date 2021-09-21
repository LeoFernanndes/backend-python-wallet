from rest_framework import routers
from people.viewsets import CustomerViewSet

router = routers.SimpleRouter()
router.register(r"customers", CustomerViewSet, basename="customer")

urlpatterns = []
urlpatterns += router.urls

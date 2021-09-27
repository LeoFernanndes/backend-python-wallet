from rest_framework import routers
from cashback.viewsets import CashbackViewset

router = routers.SimpleRouter()
router.register(r"cashbacks", CashbackViewset, basename="cashback")

urlpatterns = []
urlpatterns += router.urls

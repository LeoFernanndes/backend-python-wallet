from rest_framework import viewsets
from cashback.models import Cashback
from cashback.serializers import CashbackSerializer


class CashbackViewset(viewsets.ModelViewSet):
    serializer_class = CashbackSerializer
    queryset = Cashback.objects.all()
    http_method_names = ['get', 'post', 'head']

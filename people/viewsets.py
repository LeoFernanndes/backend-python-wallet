from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from people.models import Customer, User
from people.serializers import CustomerSerializer, UserSerializer


class CustomerViewSet(viewsets.ModelViewSet):
    serializer_class = CustomerSerializer
    queryset = Customer.objects.all()

class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()



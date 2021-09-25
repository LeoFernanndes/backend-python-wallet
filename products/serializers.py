from rest_framework import serializers, exceptions
from products.models import Product, ProductType


class ProductSerializer(serializers.ModelSerializer):
    def validate_type(self, type):
        types = [type_object.type for type_object in ProductType.objects.all()]
        if type not in types:
            raise exceptions.ValidationError('Type does not exist.')
        return type

    class Meta:
        model = Product
        fields = "__all__"


class ProductTypeSerializer(serializers.ModelSerializer):

    def validate_cashback_percent(self, cashback_percent):
        if float(cashback_percent) < 0:
            raise exceptions.ValidationError('This field must not be a negative value.')
        return cashback_percent

    def validate_type(self, type):
        types = ProductType.objects.all()
        normalized_types = [type_object.type.lower().replace(" ", "") for type_object in types]
        if type.lower().replace(" ", '') in normalized_types:
            raise exceptions.ValidationError('Type already exists.')
        return type

    class Meta:
        model = ProductType
        fields = "__all__"


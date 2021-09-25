import traceback
from rest_framework import serializers, exceptions
from rest_framework.utils import model_meta

from cashback.models import Cashback
from people.models import Customer
from products.models import Product
from products.serializers import ProductSerializer
from people.serializers import CustomerSerializer


class CashbackSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer(many=False)
    products = ProductSerializer(many=True, read_only=False, allow_null=False)


    def validate_products(self, products):
        if len(products) == 0:
            raise exceptions.ValidationError("This field must not be an empty list.")
        return products


    def validate_total(self, total):
       if total < 0:
            raise exceptions.ValidationError("This field must not be a negative sum.")
       return total


    def validate(self, attrs):
        total = self.context['request'].data['total']
        sum = float(0)
        for product in self.context['request'].data['products']:
            sum += (float(product['value']) * float(product['qty']))
        if sum != float(total):
            raise exceptions.ValidationError("Inconsistent value sum.")

        unknown = set(self.initial_data) - set(attrs.keys())
        if unknown:
            raise exceptions.ValidationError({"Unknown field(s)": "{}".format(", ".join(unknown))})
        return attrs

    class Meta:
        model = Cashback
        fields = "__all__"


    def create(self, validated_data):
        ModelClass = self.Meta.model
        try:
            customer_data = validated_data.pop('customer')
            customer = Customer.objects.create(**customer_data)
            validated_data['customer'] = customer

            products = []
            products_data_list = validated_data.pop('products')
            for products_data in products_data_list:
                product = Product.objects.create(**products_data)
                products.append(product)

            instance = ModelClass._default_manager.create(**validated_data)
            instance.products.set(products)

        except TypeError:
            tb = traceback.format_exc()
            msg = (
                    'Got a `TypeError` when calling `%s.%s.create()`. '
                    'This may be because you have a writable field on the '
                    'serializer class that is not a valid argument to '
                    '`%s.%s.create()`. You may need to make the field '
                    'read-only, or override the %s.create() method to handle '
                    'this correctly.\nOriginal exception was:\n %s' %
                    (
                        ModelClass.__name__,
                        ModelClass._default_manager.name,
                        ModelClass.__name__,
                        ModelClass._default_manager.name,
                        self.__class__.__name__,
                        tb
                    )
            )
            raise TypeError(msg)
        return instance

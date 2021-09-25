from django.db import models
from people.models import Customer
from products.models import Product


class Cashback(models.Model):
    sold_at = models.DateTimeField(null=False)
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)
    total = models.FloatField(null=False)
    products = models.ManyToManyField(Product)
    created_at = models.DateTimeField(null=True)
    message = models.CharField(max_length=255, default="Waiting for cashback api response")
    returned_id = models.IntegerField(null=True)
    cashback = models.FloatField(null=True)
    document = models.CharField(null=True, max_length=11)




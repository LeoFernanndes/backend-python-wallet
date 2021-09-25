from django.db import models
from people.models import Customer
from products.models import Product


class Cashback(models.Model):
    sold_at = models.DateTimeField(null=False)
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)
    total = models.FloatField(null=False)
    products = models.ManyToManyField(Product)

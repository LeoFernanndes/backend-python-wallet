from django.db import models


class Product(models.Model):
    type = models.CharField(max_length=255, null=False)
    value = models.FloatField(null=False)
    qty = models.IntegerField(null=False)

class ProductType(models.Model):
    type = models.CharField(max_length=255, null=False)
    cashback_percent = models.FloatField(null=False)
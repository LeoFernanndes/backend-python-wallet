from django.db import models


class Product(models.Model):
    category = models.CharField(max_length=255, null=False)
    product_name = models.CharField(max_length=255, unique=True, null=False)
    unit_value = models.FloatField(null=False)
    quantity = models.IntegerField(null=False)


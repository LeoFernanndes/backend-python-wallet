from django.db import models


class Customer(models.Model):
    name = models.CharField(max_length=255, null=False)
    document = models.CharField(max_length=11, null=False, unique=True)

from django.db import models

# Create your models here.
class Store(models.Model):
    periods = models.CharField(max_length=4000)
from django.db import models
from timeofweek.db_fields import TimeOfWeekField

# Create your models here.
class Store(models.Model):
    period = TimeOfWeekField()
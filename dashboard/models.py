from email.policy import default
from operator import mod
from statistics import mode
from django.db import models

class Holiday(models.Model):
    month_name = models.CharField(max_length=100)
    holidays = models.IntegerField(default=0)
    def __str__(self):
        return self.month_name
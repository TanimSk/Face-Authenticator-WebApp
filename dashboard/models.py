from django.db import models

class Holiday(models.Model):
    month_name = models.CharField(max_length=100)
    holidays = models.IntegerField(default=0)
    def __str__(self):
        return self.month_name

class Info(models.Model):
    name = models.CharField(max_length=20, default='main')    
    geographic_coords = models.CharField(max_length=75)
    radius = models.IntegerField()
    time_in = models.TimeField(null=True, blank=True)
    time_out = models.TimeField(null=True, blank=True)
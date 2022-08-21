from django.db import models

class Registered_user(models.Model):
    name = models.CharField(max_length=50, default='Not Given')
    email = models.CharField(max_length=100, default='Not Given')

class User_image(models.Model):
    image = models.ImageField()
    user = models.ForeignKey(Registered_user, on_delete=models.CASCADE)

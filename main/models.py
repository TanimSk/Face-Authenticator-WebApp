from django.db import models

class RegisteredUser(models.Model):
    name = models.CharField(max_length=50, default='Not Given')
    email = models.CharField(max_length=100, default='Not Given')

class UserImage(models.Model):
    image = models.ImageField(upload_to = "images/", null=True, default=None)
    user = models.ForeignKey(RegisteredUser, on_delete=models.CASCADE, related_name='user_images')

class Log(models.Model):
    name = models.CharField(max_length=60, default='Not Given')
    time_in = models.DateTimeField(auto_now_add=True)
    time_out = models.CharField(max_length=60, default=' - ')

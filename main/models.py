from django.db import models

class RegisteredUser(models.Model):
    name = models.CharField(max_length=100, default='Not Given')
    email = models.CharField(max_length=100, default='Not Given')
    department = models.CharField(max_length=100, default='Not Given')
    def __str__(self):
        return self.name


class UserImage(models.Model):
    image = models.ImageField(upload_to = "images/", null=True, default=None)
    user = models.ForeignKey(RegisteredUser, on_delete=models.CASCADE, related_name='user_images')


class Log(models.Model):

    name = models.CharField(max_length=60, default='Not Given')

    time_in = models.DateTimeField(null=True, blank=True)
    late_join = models.BooleanField(default=False, null=True, blank=True)
    location_in = models.CharField(max_length=500, null=True, blank=True)
    location_in_url = models.CharField(max_length=500, null=True, blank=True)
    delay_in = models.CharField(max_length=50, default='-', null=True)

    time_out = models.DateTimeField(null=True, blank=True)
    late_leave = models.BooleanField(default=False, null=True, blank=True)
    location_out = models.CharField(max_length=500, null=True, blank=True)
    location_out_url = models.CharField(max_length=500, null=True, blank=True)
    delay_out = models.CharField(max_length=50, default='-', null=True)

    total_hours = models.CharField(max_length=50, default='-', null=True)
    approved = models.BooleanField(default=True, blank=True)
    user = models.ForeignKey(RegisteredUser, on_delete=models.CASCADE, related_name='user_logs')


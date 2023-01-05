from django.contrib import admin
from .models import *


class RegisteredUserAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "department", )


class UserImageAdmin(admin.ModelAdmin):
    list_display = ('user', "image", )


class LogAdmin(admin.ModelAdmin):
    list_display = \
        ('name',
         'time_in', 'location_in', 'delay_in',
         'time_out', 'location_out', 'delay_out',
         'total_hours', 'user',)


admin.site.register(RegisteredUser, RegisteredUserAdmin)
admin.site.register(UserImage, UserImageAdmin)
admin.site.register(Log, LogAdmin)

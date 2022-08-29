from modulefinder import Module
from django.contrib import admin
from .models import *

class RegisteredUserAdmin(admin.ModelAdmin):
    list_display = ("name", "email", )

class UserImageAdmin(admin.ModelAdmin):
    list_display = ('user', "image", )

class LogAdmin(admin.ModelAdmin):
    list_display = \
    ('name',
    'time_in', 'late_join', 'location_in', 'delay_in',
    'time_out', 'late_leave', 'location_out', 'delay_out',
    'total_hours', 'user',)

class TimingAdmin(admin.ModelAdmin):
    list_display = ('name', 'time_in', 'time_out',)


admin.site.register(RegisteredUser, RegisteredUserAdmin)
admin.site.register(UserImage, UserImageAdmin)
admin.site.register(Log, LogAdmin)
admin.site.register(Timing, TimingAdmin)

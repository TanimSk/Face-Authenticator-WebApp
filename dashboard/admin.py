from django.contrib import admin
from .models import Holiday


class HolidayAdmin(admin.ModelAdmin):
    list_display = ("month_name", "holidays")


admin.site.register(Holiday, HolidayAdmin)

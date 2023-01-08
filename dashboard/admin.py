from django.contrib import admin
from django import forms
from .models import Holiday, Info


@admin.register(Holiday)
class HolidayAdmin(admin.ModelAdmin):
    list_display = ("month_name", "holidays")


@admin.register(Info)
class InfoAdmin(admin.ModelAdmin):
    list_display = ("name", "time_in", "time_out",
                    "radius", "geographic_coords", )

    def get_form(self, request, obj=None, **kwargs):
        kwargs['widgets'] = {
            'radius': forms.NumberInput(attrs={'placeholder': 'in metre'})
        }
        return super().get_form(request, obj, **kwargs)

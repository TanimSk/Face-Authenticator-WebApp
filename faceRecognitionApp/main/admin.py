from django.contrib import admin
from .models import RegisteredUser, UserImage

class RegisteredUserAdmin(admin.ModelAdmin):
    list_display = ("name", "email", )
class UserImageAdmin(admin.ModelAdmin):
    list_display = ('user', "image", )


admin.site.register(RegisteredUser, RegisteredUserAdmin)
admin.site.register(UserImage, UserImageAdmin)
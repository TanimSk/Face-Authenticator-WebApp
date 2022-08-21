from django.contrib import admin
from django.urls import path
from main import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.form, name='form'),
    path('register/', views.register, name='register'),
]

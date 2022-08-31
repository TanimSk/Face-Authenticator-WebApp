from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from main import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('signin/', views.sign_in, name='signin'),
    path('signout/', views.sign_out, name='signout'),
    path('register/', views.register, name='register'),
    path('dashboard-today/', views.dashboard_today, name='dashboard-today'),
    path('dashboard-master/', views.dashboard_master, name='dashboard-master'),
    path('login', views.auth_login, name='login'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

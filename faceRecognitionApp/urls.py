from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from main import views as main_view
from dashboard import views as dashboard_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', main_view.home, name='home'),
    path('signin/', main_view.sign_in, name='signin'),
    path('signout/', main_view.sign_out, name='signout'),
    path('register/', main_view.register, name='register'),
    path('login', main_view.auth_login, name='login'),

    path('dashboard/', dashboard_view.dashboard, name='dashboard'),
    path('dashboard-today/', dashboard_view.dashboard_today, name='dashboard-today'),
    path('dashboard-master/', dashboard_view.dashboard_master, name='dashboard-master'),
    path('generate-report/', dashboard_view.generate_report, name='generate-report'),
    path('generate-report/<int:days>', dashboard_view.generate_report, name='generate-report'),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

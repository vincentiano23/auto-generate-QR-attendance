from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register_view, name='register'), 
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('register/', views.register_student, name='register_student'),
    path('logout/', views.logout_view, name='logout'),
    path('registration-success/', views.registration_success, name='registration_success'), 
    path('generate_qr_code/<int:student_id>/', views.generate_qr_code, name='generate_qr_code'),
    path('scan_qr_code/', views.scan_qr_code, name='scan_qr_code'),
    path('attendance_stats/', views.attendance_stats, name='attendance_stats'),
    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

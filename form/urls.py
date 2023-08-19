from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_user, name='login'),
    path('display/', views.contact_display_view, name='display'),
    path('', views.contact_view, name='contact'),
    path('success/', views.success, name='success')
]

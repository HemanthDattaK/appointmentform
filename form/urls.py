from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_user, name='login'),
    path('display/', views.contact_display_view, name='display'),
    path('', views.contact_view, name='contact'),
    path('success/', views.success, name='success'),
    path('set/', views.set_appointment_times, name='set_times'),
    path('after/', views.afterview, name='after'), 
    path('delete_contact/', views.contact_display_view, name='contact_delete'),
    path('meeting/', views.meeting, name='meeting'),  
    path('help/', views.help, name='help'),  
    path('authorize/', views.authorize_meeting, name='authorize_meeting'),

]

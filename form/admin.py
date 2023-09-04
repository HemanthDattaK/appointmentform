from django.contrib import admin

# Register your models here.
# admin.py

from django.contrib import admin
from .models import Contact, AppointmentLimit

admin.site.register(Contact)
admin.site.register(AppointmentLimit)

# forms.py

from django import forms
from .models import Contact


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'surname', 'phonenumber', 'place', 'purpose', 'date']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }

# forms.py

class AppointmentTimeForm(forms.Form):
    start_time = forms.TimeField(label='Appointment Start Time')
    end_time = forms.TimeField(label='Appointment End Time')
    appointment_limit = forms.IntegerField(label='Appointment Limit', min_value=1)

from django.http import HttpResponseBadRequest
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib import messages
from .models import AppointmentLimit, Contact  # Assuming your Contact model is in the same app
from .forms import AppointmentTimeForm, ContactForm  # Import your ContactForm
from twilio.rest import Client
from datetime import datetime, timedelta
from django.conf import settings


from django.http import HttpResponseBadRequest
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import ContactForm
from .models import AppointmentLimit, Contact
from .utils import send_sms  # Import your send_sms function
from datetime import datetime, timedelta
from django.conf import settings

def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            contact = form.save(commit=False)

            # Calculate appointment time based on the admin settings
            start_time = datetime.strptime(settings.APPOINTMENT_START_TIME, '%H:%M')
            end_time = datetime.strptime(settings.APPOINTMENT_END_TIME, '%H:%M')
            interval = timedelta(minutes=10)  # Set the interval to 10 minutes
            appointment_time = start_time

            # Check if there is an appointment limit record
            appointment_limit = AppointmentLimit.objects.first()

            if appointment_limit:
                # Check if the appointment limit is reached for the selected date and time range
                selected_date = contact.date
                appointments_on_date = Contact.objects.filter(date=selected_date).count()

                if appointments_on_date >= appointment_limit.limit:
                    return HttpResponseBadRequest("Appointment limit for this date has been reached.")

                # Check if the appointment limit is reached for the selected time range
                appointments_in_time_range = Contact.objects.filter(
                    date=selected_date,
                    time_slot_choice__gte=start_time.strftime('%H:%M'),
                    time_slot_choice__lte=end_time.strftime('%H:%M')
                ).count()

                if appointments_in_time_range >= appointment_limit.limit:
                    return HttpResponseBadRequest("Appointment limit for this time range has been reached.")
            
            # Find the next available time slot within the specified time range
            while appointment_time <= end_time:
                existing_contacts = Contact.objects.filter(date=contact.date, time_slot_choice=appointment_time.strftime('%H:%M'))
                if existing_contacts.exists():
                    appointment_time += interval
                else:
                    contact.time_slot_choice = appointment_time.strftime('%H:%M')
                    break

            contact.save()  # Save the form data
            
            try:
                send_sms(contact.phonenumber, contact.name, contact.date, contact.time_slot_choice)  # Send SMS with details
            except Exception as e:
                # Handle the exception if SMS sending fails (you can log the error)
                pass

            allocated_time = contact.time_slot_choice  # Store the allocated time in a variable

            # Store the allocated time and other data in the session
            request.session['allocated_time'] = allocated_time
            request.session['name'] = contact.name
            request.session['surname'] = contact.surname
            request.session['phonenumber'] = contact.phonenumber
            request.session['place'] = contact.place
            request.session['purpose'] = contact.purpose
            request.session['date'] = contact.date.strftime('%Y-%m-%d')
            
            # Redirect to the success page
            return redirect('success')

        else:
            # Handle the form not being valid
            messages.error(request, 'Invalid form data. Please check the fields.')
    else:
        form = ContactForm()

    return render(request, 'fill.html', {'form': form})




def set_appointment_times(request):
    if request.method == 'POST':
        form = AppointmentTimeForm(request.POST)
        if form.is_valid():
            start_time = form.cleaned_data['start_time']
            end_time = form.cleaned_data['end_time']
            appointment_limit = form.cleaned_data['appointment_limit']

            # Validate the input (e.g., start time should be before end time)
            if start_time >= end_time:
                messages.error(request, 'Invalid time range. Start time should be before end time.')
            elif appointment_limit <= 0:
                messages.error(request, 'Invalid appointment limit. It should be greater than zero.')
            else:
                # Update the Django settings
                settings.APPOINTMENT_START_TIME = start_time.strftime('%H:%M')
                settings.APPOINTMENT_END_TIME = end_time.strftime('%H:%M')
                settings.APPOINTMENT_LIMIT = appointment_limit
                messages.success(request, 'Appointment settings updated successfully.')
                return redirect('success')
        else:
            messages.error(request, 'Invalid form data. Please check the fields.')
    else:
        form = AppointmentTimeForm()

    return render(request, 'set.html', {'form': form})

def contact_display_view(request):
    if request.method == 'POST':
        contact_id = request.POST.get('contact_id')  # Assuming you have an input field with 'contact_id' in your template
        try:
            contact = Contact.objects.get(id=contact_id)
            contact.delete()
        except Contact.DoesNotExist:
            pass  # Handle the case where the contact doesn't exist (optional)
    
    contacts = Contact.objects.all()
    return render(request, 'display.html', {'contacts': contacts})

def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('after')
        else:
            messages.error(request, 'Invalid credentials. Please try again.')
    
    return render(request, 'login.html')

def success(request):
    allocated_time = request.session.get('allocated_time', None)
    name = request.session.get('name', None)
    surname = request.session.get('surname', None)
    phonenumber = request.session.get('phonenumber', None)
    place = request.session.get('place', None)
    purpose = request.session.get('purpose', None)
    date_str = request.session.get('date', None)
    date = datetime.strptime(date_str, '%Y-%m-%d').date() if date_str else None

    # Clear the session variables to avoid displaying the same data on subsequent visits
    if allocated_time:
        del request.session['allocated_time']
    if name:
        del request.session['name']
    if surname:
        del request.session['surname']
    if phonenumber:
        del request.session['phonenumber']
    if place:
        del request.session['place']
    if purpose:
        del request.session['purpose']
    if date:
        del request.session['date']

    return render(request, 'success.html', {
        'allocated_time': allocated_time,
        'name': name,
        'surname': surname,
        'phonenumber': phonenumber,
        'place': place,
        'purpose': purpose,
        'date': date,
  })

def send_sms(phone_number, name, date, time_slot):
    # Replace the following with your Twilio credentials
    account_sid = 'ACff5cae06c392b64945d30c3014eea14c'
    auth_token = '84d1947cf57ea3ffffb118e54d774599'
    twilio_phone_number = '+14707480390'

    client = Client(account_sid, auth_token)

    if phone_number.startswith('+'):
        country_code = ''
 
    else:
        country_code = '+91'

    #Replace 'Your SMS content here' with your actual SMS content
    sms_content = f'Dear {name} Your Appointment Is Successfully Booked at \nDate: {date}\nTime: {time_slot}'

    # Send the SMS using Twilio
    client.messages.create(
        to=country_code + phone_number,
        from_=twilio_phone_number,
        body=sms_content
    )



def set_appointment_limits(request):
    appointment_limit = AppointmentLimit.objects.first()

    if request.method == 'POST':
        form = AppointmentLimit(request.POST, instance=appointment_limit)
        if form.is_valid():
            form.save()
            return redirect('set_appointment_limits')  # Redirect back to the same page after saving
    else:
        form = AppointmentLimit(instance=appointment_limit)

    return render(request, 'set_appointment_limits.html', {'form': form})

def afterview(request):
    return render(request,'admin.html')

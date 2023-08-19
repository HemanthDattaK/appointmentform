from django.shortcuts import render, redirect
from django.contrib.auth import login,authenticate
from form.models import Contact
from .forms import ContactForm
from django.contrib import messages

def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('success')  # Redirect to a success page
    else:
        form = ContactForm()
    return render(request, 'fill.html', {'form': form})


def contact_display_view(request):
    contacts = Contact.objects.all()
    return render(request, 'display.html', {'contacts': contacts})

def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('display')
        else:
            messages.error(request, 'Invalid credentials. Please try again.')
    
    return render(request, 'login.html')

def success(request):
    return render(request, 'success.html')
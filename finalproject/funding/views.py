import re
from django.shortcuts import render, redirect
from .models import *

# Create your views here.
def index(request):
    return render(request, 'funding/index.html')

def register(request):
    errors = {}
    data = {}
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name'] 
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        phone = request.POST['phone']
        picture = request.FILES.get('picture')

        if not first_name:
            errors['first_name'] = "First name is required."
        else:
            data['first_name'] = first_name
        
        if not last_name:
            errors['last_name'] = "Last name is required."
        else:
            data['last_name'] = last_name

        if not email:
            errors['email'] = "Email is required."
        elif "@" not in email or "." not in email:
            errors['email'] = "Enter a valid email address."
        else:
            data['email'] = email

        if not password:
            errors['password'] = "Password is required."
        else:
            data['password'] = password
        
        if not confirm_password:
            errors['confirm_password'] = "Confirm password is required."
        elif confirm_password != password:
            errors['confirm_password'] = "Passwords do not match."
        else:
            data['confirm_password'] = confirm_password

        egyptian_phone_pattern = r"^01[0125]\d{8}$"

        if not phone:
            errors['phone'] = "Phone is required."
        elif not re.match(egyptian_phone_pattern, phone):
            errors['phone'] = "Enter a valid phone number."
        else:
            data['phone'] = phone
        
        if not picture:
            errors['picture'] = "Profile picture is required."
        else:
            data['picture'] = picture

        if errors:
            return render(request, 'funding/register.html', {'errors': errors, 'data': data})
        else:
            user = UserProfile.objects.create(
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password, 
            phone=phone,
            picture=picture
        )
            
            return redirect('login')
    return render(request, 'funding/register.html')

def login(request):
    return render(request, 'funding/login.html')

def logout(request):
    return render(request, 'funding/logout.html')
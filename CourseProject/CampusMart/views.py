from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import check_password
from django.core.exceptions import ValidationError
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.models import User

# Create your views here.

def index(request):
    first_name = ""
    
    if request.user.is_authenticated:
        first_name = request.user.first_name

    context = {
        'app': 'Campus Mart',
        'first_name': first_name,
    }
    return render(request, 'CampusMart/index.html', context)

def login_view(request):
    errors = None
    if request.method == 'POST':
        # Get user credentials from POST request
        uname = request.POST["username"]
        pwd = request.POST["password"]

        # Authenticate user using Django's built-in authenticate method
        user = authenticate(request, username=uname, password=pwd)

        if user is not None:
            # User is authenticated, log them in
            login(request, user)
            return HttpResponseRedirect(reverse('CampusMart:index'))
        else:
            messages.error(request, 'Login failed. Please check your username and password.')
            errors = [('authentication', "Login error")]

    return render(request, 'CampusMart/login.html', {'errors': errors})

def logout_view(request):
    # Logout the user using Django's built-in logout function
    logout(request)
    messages.success(request, 'Log out was successful!')
    return HttpResponseRedirect(reverse("CampusMart:login"))

def register(request):
    if request.method == 'POST':
        # Create a model instance and populate it with data from the request
        first_name = request.POST["first_name"]
        uname = request.POST["username"]
        pwd = request.POST["password"]
        email = request.POST["email"]

        try:
            # Create a new user using Django's create_user method (which hashes the password)
            user = User.objects.create_user(username=uname, password=pwd, email=email)
            user.first_name = first_name

            # If we reach here, the validation succeeded
            user.save()  # Save the new user to the database
            # Redirect to the login page
            return HttpResponseRedirect(reverse('CampusMart:login'))

        except ValidationError as e:
            # Handle validation errors
            return HttpResponseRedirect(reverse('CampusMart:index'))
    else:
        return render(request, "CampusMart/register.html")

from django.shortcuts import render, get_object_or_404
from django.urls import reverse
#from .models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import check_password, make_password
from django.core.exceptions import ValidationError
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.models import User

# Create your views here.

def index(request):
    context = {'app': 'Campus Mart'}
    return render(request, 'CampusMart/index.html', context)

def register(request):
    if request.POST:
        # Create a model instance and populate it with data from the request
        name = request.POST["name"]
        uname = request.POST["username"]
        pwd = request.POST["password"]
        email = request.POST["email"]

        user = User(username=uname, password=pwd, email=email)

        try:
            user.full_clean()
            user.password = make_password(pwd)  # encrypts
            # if we reach here, the validation succeeded
            user.save()  # saves on the db
            # redirect to the login page
            return HttpResponseRedirect(reverse('CampusMart:login'))
        
        except ValidationError as e:
            pass # do something with it, as you wish

    else:
        return render(request, "CampusMart/register.html")


def login_view(request):
    if request.POST:
        uname = request.POST["username"]
        pwd = request.POST["password"]

        user = authenticate(request, username=uname, password=pwd)
        print("Authenticated user:", user)

        if user is not None:
            login(request, user)  # Logs the user in
            return HttpResponseRedirect(reverse('CampusMart:index'))  # Redirect to index page after successful login
        else:
            # Add a message for failed login attempt
            messages.error(request, "Invalid username or password. Please try again.")
            return HttpResponseRedirect(reverse('CampusMart:login'))  # Redirect back to login if failed
    else:
        return render(request, "CampusMart/login.html")
        
    
def logout_view(request):
    logout(request)
    return render(request, "CampusMart/logout.html")
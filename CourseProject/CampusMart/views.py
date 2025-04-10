from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import check_password
from django.core.exceptions import ValidationError
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.models import User

# index view
def index(request):
    first_name = ""
    
    if request.user.is_authenticated:
        first_name = request.user.first_name

    context = {
        'app': 'Campus Mart',
        'first_name': first_name,
    }

    return render(request, 'CampusMart/index.html', context)
# login view
def login_view(request):
    errors = None
    if request.method == 'POST':
        # get user credentials from POST request
        uname = request.POST["username"]
        pwd = request.POST["password"]

        # authenticate user using authenticate method
        user = authenticate(request, username=uname, password=pwd)

        if user is not None:
            # user is authenticated, log them in
            login(request, user)
            return HttpResponseRedirect(reverse('CampusMart:index'))
        else:
            # user is not authenticated, display error
            messages.error(request, 'Login failed. Please check your username and password.')
            errors = [('authentication', "Login error")]

    return render(request, 'CampusMart/login.html', {'errors': errors})

# log out view
def logout_view(request):
    # logout user using logout function
    logout(request)
    messages.success(request, 'Log out was successful!')
    return HttpResponseRedirect(reverse("CampusMart:login"))

def register(request):
    if request.method == 'POST':
        # get user credentials from POST request
        first_name = request.POST["first_name"]
        uname = request.POST["username"]
        pwd = request.POST["password"]
        email = request.POST["email"]

        try:
            # create a new user
            user = User.objects.create_user(username=uname, password=pwd, email=email)
            user.first_name = first_name

            # validation succeeded, save the new user to the database
            user.save()
            # redirect to the login page
            return HttpResponseRedirect(reverse('CampusMart:login'))

        except ValidationError as e:
            # handle validation errors
            return HttpResponseRedirect(reverse('CampusMart:index'))
    else:
        return render(request, "CampusMart/register.html")

from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import check_password
from django.core.exceptions import ValidationError
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.models import User as AuthUser
from .models import Product, ProductImage, User
from django.contrib.auth.decorators import login_required
from django.utils.timezone import now
from django.core.paginator import Paginator
from django.shortcuts import render 

# index view
def index(request):
    first_name = ""
    
    if request.user.is_authenticated:
        try:
            custom_user = User.objects.get(auth_user=request.user)
            first_name = custom_user.first_name
        except User.DoesNotExist:
            first_name = request.user.first_name or request.user.username

    context = {
        'app': 'CampusMart',
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

# register view
def register(request):
    if request.method == 'POST':
        # get user credentials from POST request
        first_name = request.POST["first_name"]
        uname = request.POST["username"]
        pwd = request.POST["password"]
        email = request.POST["email"]

        try:
            # create a new user
            auth_user = AuthUser.objects.create_user(username=uname, password=pwd, email=email)
            user = User.objects.create(auth_user=auth_user, username=uname, email=email)
            #user = User.objects.create_user(username=uname, password=pwd, email=email)
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

# create listing
def create_listing(request):
    today = now().date()
    try:
        seller_user = User.objects.get(auth_user=request.user)
    except User.DoesNotExist:
        return render(request, 'CampusMart/create_listing.html', {
            'remaining': 0,
            'error': 'Your user profile was not found.'
        })
    post_count = Product.objects.filter(seller=seller_user, post_date__date=today).count()

    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        price = request.POST.get('price')
        condition = request.POST.get('condition')
        images = request.FILES.getlist('images')

        if not title or not description or not price or not condition or not images:
            messages.error(request, "All fields are required, including at least one image.")
            return render(request, 'CampusMart/create_listing.html')

        if post_count >= 3:
            messages.warning(request, "You've reached your daily listing limit.")
            return HttpResponseRedirect(reverse('CampusMart:index'))
        
        product = Product.objects.create(
            seller=seller_user,
            title=title,
            description=description,
            price=price,
            condition=condition,
            post_date = today,
            status='AVAILABLE'
        )

        for img in request.FILES.getlist('images'):
            ProductImage.objects.create(product=product, image=img)

        return HttpResponseRedirect(reverse('CampusMart:index'))
    
    context = {
        'remaining': 3 - post_count,
    }
    

    return render(request, 'CampusMart/create_listing.html', context)

# update listing
@login_required
def update_listing(request, product_id):
    today = now().date()
    try:
        seller_user = User.objects.get(auth_user=request.user)
    except User.DoesNotExist:
        return render(request, 'CampusMart/create_listing.html', {
            'remaining': 0,
            'error': 'Your user profile was not found.'
        })
    product = get_object_or_404(Product, id=product_id, seller__auth_user=request.user)
    post_count = Product.objects.filter(seller=seller_user, post_date__date=today).count()

    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        price = request.POST.get('price')
        condition = request.POST.get('condition')
        status = request.POST.get('status')
        new_images = request.FILES.getlist('images')

        if not title or not description or not price or not condition or not status:
            return HttpResponseRedirect(reverse('CampusMart:index'))

        # Update fields
        product.title = title
        product.description = description
        product.price = price
        product.condition = condition
        product.status = status
        product.save()

        if new_images:
            ProductImage.objects.filter(product=product).delete()
            for img in new_images:
                ProductImage.objects.create(product=product, image=img)
        return HttpResponseRedirect(reverse('CampusMart:index'))

    context = {
        'product': product,
        'remaining': 3 - Product.objects.filter(seller=product.seller, post_date__date=now().date()).count(),
    }

    return render(request, 'CampusMart/update_listing.html', context)


@login_required
def my_listings(request):
    try:
        user_profile = User.objects.get(auth_user=request.user)
    except User.DoesNotExist:
        return render(request, 'CampusMart/my_listings.html', {'error': 'Profile not found', 'listings': []})

    listings = Product.objects.filter(seller=user_profile)

    return render(request, 'CampusMart/my_listings.html', {
        'listings': listings
    })

@login_required
def delete_listing(request, product_id):
    try:
        # Get the custom user linked to the logged-in Django user
        custom_user = User.objects.get(auth_user=request.user)
    except User.DoesNotExist:
        return HttpResponseRedirect(reverse('CampusMart:my_listings'))

    # Get the product only if it belongs to the current user
    try:
        product = Product.objects.get(id=product_id, seller=custom_user)
    except Product.DoesNotExist:
        return HttpResponseRedirect(reverse('CampusMart:my_listings'))

    # Delete only on POST
    if request.method == 'POST':
        product.delete()
        return HttpResponseRedirect(reverse('CampusMart:my_listings'))

    # Fallback (not expected)
    return HttpResponseRedirect(reverse('CampusMart:my_listings'))


#view all listings 
def view_all(request):
    #get all listings available
    listings = Product.objects.all()  
    #use paginator to get 20 per page
    p = Paginator(listings, 20)    
    #to help users navigate 
    page_number = request.GET.get("page")
    page_obj = p.get_page(page_number)        

    return render(request, 'CampusMart/view_all.html', {'listings': listings, 'page_obj': page_obj})
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import check_password
from django.core.exceptions import ValidationError
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.models import User as AuthUser
from .models import Product, ProductImage, User, Message
from django.contrib.auth.decorators import login_required
from django.utils.timezone import now
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib import messages
from .forms import PurchaseListingsForm
from .models import UserExtraListings
from .services import get_access_token, view_balance_for_user, user_pay
from django.conf import settings
from django.utils.timezone import localtime

# index view
def index(request):
    first_name = ""
    remaining = 0
    
    if request.user.is_authenticated:
        try:
            custom_user = User.objects.get(auth_user=request.user)
            first_name = custom_user.first_name
            today = localtime().date()
            post_count = Product.objects.filter(seller=custom_user, post_date__date=today).count()
            user = UserExtraListings.objects.get_or_create(user=custom_user)[0]
            remaining = max(0, 3 + user.extra_listings - post_count)

        except User.DoesNotExist:
            first_name = request.user.first_name or request.user.username

    context = {
        'app': 'CampusMart',
        'first_name': first_name,
        'remaining': remaining,
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
            user.first_name = first_name

            # validation succeeded, save the new user to the database
            user.save()
            # redirect to the login page
            return HttpResponseRedirect(reverse('CampusMart:login'))

        except ValidationError as e:
            # handle validation errors
            messages.error(request, "Registration failed. Please correct the errors and try again.")
            return render(request, "CampusMart/register.html")
        except Exception as e:
            messages.error(request, f"Error: Name already exists in database. Try again.")
            return render(request, "CampusMart/register.html")
    else:
        return render(request, "CampusMart/register.html")

# create listing
@login_required
def create_listing(request):
    today = localtime().date()
    try:
        seller_user = User.objects.get(auth_user=request.user)
    except User.DoesNotExist:
        return render(request, 'CampusMart/create_listing.html', {
            'remaining': 0,
            'error': 'Your user profile was not found.'
        })
    
    # get remaining listings
    post_count = Product.objects.filter(seller=seller_user, post_date__date=today).count()
    user = UserExtraListings.objects.get_or_create(user=seller_user)[0]
    remaining = max(0, 3 + user.extra_listings - post_count)

    # get all info
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        price = request.POST.get('price')
        condition = request.POST.get('condition')
        images = request.FILES.getlist('images')

        if not title or not description or not price or not condition or not images:
            messages.error(request, "All fields are required, including at least one image.")
            return render(request, 'CampusMart/create_listing.html')

        if remaining <= 0:
            messages.warning(request, "You've reached your daily listing limit.")
            return HttpResponseRedirect(reverse('CampusMart:index'))
        
        product = Product.objects.create(
            seller=seller_user,
            title=title,
            description=description,
            price=price,
            condition=condition,
            post_date = localtime(),
            status='AVAILABLE'
        )
        post_count = Product.objects.filter(seller=seller_user, post_date__date=today).count()

        messages.success(request, "Listing Successfully Posted")

        for img in request.FILES.getlist('images'):
            ProductImage.objects.create(product=product, image=img)

        return HttpResponseRedirect(reverse('CampusMart:index'))
    
    context = {
        'remaining': remaining,
    }
    
    return render(request, 'CampusMart/create_listing.html', context)

# update listing
@login_required
def update_listing(request, product_id):
    today = localtime().date()
    try:
        seller_user = User.objects.get(auth_user=request.user)
    except User.DoesNotExist:
        return render(request, 'CampusMart/create_listing.html', {
            'remaining': 0,
            'error': 'Your user profile was not found.'
        })
    product = get_object_or_404(Product, id=product_id, seller__auth_user=request.user)
    post_count = Product.objects.filter(seller=seller_user, post_date__date=today).count()

    # get all info
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        price = request.POST.get('price')
        condition = request.POST.get('condition')
        status = request.POST.get('status')
        new_images = request.FILES.getlist('images')

        if not title or not description or not price or not condition or not status:
            return HttpResponseRedirect(reverse('CampusMart:index'))

        # update fields
        product.title = title
        product.description = description
        product.price = price
        product.condition = condition
        product.status = status
        product.save()
        messages.success(request, "Listing Successfully Updated")

        if new_images:
            ProductImage.objects.filter(product=product).delete()
            for img in new_images:
                ProductImage.objects.create(product=product, image=img)
        return HttpResponseRedirect(reverse('CampusMart:index'))

    context = {
        'product': product,
        'remaining': 3 - Product.objects.filter(seller=product.seller, post_date__date=localtime().date()).count(),
    }

    return render(request, 'CampusMart/update_listing.html', context)

# my listings
@login_required
def my_listings(request):
    try:
        user_profile = User.objects.get(auth_user=request.user)
    except User.DoesNotExist:
        return render(request, 'CampusMart/my_listings.html', {'error': 'Profile not found', 'listings': []})

    # get all listings based on profile
    listings = Product.objects.filter(seller=user_profile)

    return render(request, 'CampusMart/my_listings.html', {
        'listings': listings
    })

# delete listing
@login_required
def delete_listing(request, product_id):
    try:
        # get the user linked to the logged-in user
        custom_user = User.objects.get(auth_user=request.user)
    except User.DoesNotExist:
        return HttpResponseRedirect(reverse('CampusMart:my_listings'))

    # get the product only if it belongs to the current user
    try:
        product = Product.objects.get(id=product_id, seller=custom_user)
    except Product.DoesNotExist:
        return HttpResponseRedirect(reverse('CampusMart:my_listings'))

    # delete only on POST
    if request.method == 'POST':
        product.delete()
        return HttpResponseRedirect(reverse('CampusMart:my_listings'))

    return HttpResponseRedirect(reverse('CampusMart:my_listings'))


# view all listings 
def view_all(request):
    query = request.GET.get('q')

    # filter listings based on query
    listings = Product.objects.filter(status='AVAILABLE')
    if query:
        listings = listings.filter(
            Q(title__icontains=query) | Q(description__icontains=query)
        )

    listings = listings.order_by('-post_date')  # sort after filtering

    # paginate the (filtered) listings
    p = Paginator(listings, 20)
    page_number = request.GET.get("page")
    page_obj = p.get_page(page_number)

    return render(request, 'CampusMart/view_all.html', {
        'page_obj': page_obj,
        'query': query,  # send back query to maintain it in pagination links if needed
    })

# message function between seller & buyer
@login_required
def messaging(request, product_id):
    sender_user = get_object_or_404(User, auth_user=request.user)
    if request.method == 'POST':
        product = get_object_or_404(Product, id=product_id)
        sender_user = User.objects.get(auth_user=request.user)
        receiver_user = product.seller

        body = request.POST.get('body')

        # get the messages sent/received attached to current user
        if body:
            Message.objects.create(
                sender=sender_user,
                receiver=receiver_user,
                product=product,
                body=body
            )
            messages.success(request, "Message sent!")
            return HttpResponseRedirect(reverse('CampusMart:view_all'))
        
        else:
            return HttpResponseRedirect(reverse('CampusMart:view_all'))

    return HttpResponseRedirect(reverse('CampusMart:view_all'))

# inbox view to view the messages
@login_required
def inbox(request):
    try:
        user = User.objects.get(auth_user=request.user)
    except User.DoesNotExist:
        return HttpResponseRedirect(reverse('CampusMart:index'))

    # sort the messages
    all_messages = Message.objects.filter(Q(sender=user) | Q(receiver=user)).order_by('-timestamp')

    conversations = {}

    for msg in all_messages:
        participants = tuple(sorted([msg.sender.id, msg.receiver.id]))
        key = (participants, msg.product.id)

        if key not in conversations:
            conversations[key] = msg  # first (latest) message seen

    context = {
        'conversations': conversations.values()
    }
    return render(request, 'CampusMart/messaging.html', context)

@login_required
def chat_with_user(request, product_id, user_id):
    try:
        user = User.objects.get(auth_user=request.user) 
        other_user = User.objects.get(id=user_id)         # user you're chatting with
        product = Product.objects.get(id=product_id)      # product we're chatting about
    except (User.DoesNotExist, Product.DoesNotExist):
        messages.error(request, "User or product not found.")
        return redirect('CampusMart:inbox')

    # get all messages between these two users about product
    chat_messages = Message.objects.filter(product=product).filter((Q(sender=user) & Q(receiver=other_user)) |(Q(sender=other_user) & Q(receiver=user))).order_by('timestamp')  # sort oldest to newest

    if request.method == 'POST':
        body = request.POST.get('body')
        if body:
            Message.objects.create(
                sender=user,
                receiver=other_user,
                product=product,
                body=body
            )
            return redirect('CampusMart:chat_with_user', product_id=product.id, user_id=other_user.id)

    return render(request, 'CampusMart/chat.html', {
        'other_user': other_user,
        'chat_messages': chat_messages,
        'product': product,
    })

# purchasing interface view 
def purchase_listings(request):
    balance = None     # default balance
    listing_balance = None  # user's current balance

    if request.user.is_authenticated:
        user_email = request.user.email
        # get current listing balance
        try:
            user = User.objects.get(email=user_email)
            user_extra = UserExtraListings.objects.get(user=user)
            listing_balance = user_extra.extra_listings
        except (User.DoesNotExist, UserExtraListings.DoesNotExist):
            listing_balance = 0
        # get external balance
        try:
            access_token = get_access_token(settings.API_USERNAME, settings.API_PASSWORD)
            balance = view_balance_for_user(access_token, user_email)
        except Exception as e:
            balance = "Unavailable"
            messages.error(request, f"Could not retrieve balance: {str(e)}")

    if request.method == 'POST':
        form = PurchaseListingsForm(request.POST)
        if form.is_valid():
            number_of_listings = form.cleaned_data['number_of_listings']
            user_email = request.user.email

            try:
                # get Access Token
                access_token = get_access_token(settings.API_USERNAME, settings.API_PASSWORD)

                # view Current Balance
                balance = view_balance_for_user(access_token, user_email)

                # check if user has enough balance
                if balance is None:
                    messages.error(request, "Could not retrieve your balance. Please try again later.")
                    return redirect('CampusMart:purchase_listings')
                if balance < number_of_listings:
                    messages.error(request, "Insufficient funds.")
                    return redirect('CampusMart:purchase_listings')

                # charge the user
                user_pay(access_token, user_email, number_of_listings)

                # update user's extra listings locally
                user = User.objects.get(email=user_email)
                extra_listing_record, created = UserExtraListings.objects.get_or_create(user=user)
                extra_listing_record.extra_listings += number_of_listings
                extra_listing_record.save()

                messages.success(request, f"You successfully purchased {number_of_listings} extra listings!")

            except Exception as e:
                messages.error(request, f"An error occurred: {str(e)}")

            return redirect('CampusMart:purchase_listings')
    else:
        form = PurchaseListingsForm()

    return render(request, 'CampusMart/purchase_listings.html', {'form': form, 'balance': balance, 'listing_balance': listing_balance,})

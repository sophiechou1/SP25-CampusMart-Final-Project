from django.db import models
from django.contrib.auth.models import User as AuthUser
import os
from django.utils.timezone import now


# user model
class User(models.Model):
    auth_user = models.OneToOneField(AuthUser, on_delete=models.CASCADE, null=True, blank=True)
    first_name = models.CharField(max_length=30, null=True, default="Default Name")
    username = models.CharField(max_length=200, unique=True)
    password = models.TextField()
    email = models.EmailField(max_length=200, unique=True)

    def __str__(self):
        return self.username

# product model 
class Product(models.Model):
    CONDITION_CHOICES = [
        ('NEW', 'New'),
        ('LIKE_NEW', 'Like New'),
        ('USED', 'Used'),
        ('FAIR', 'Fair'),
    ]
    seller = models.ForeignKey(User, on_delete=models.CASCADE)
    post_date = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    condition = models.CharField(max_length=10, choices=CONDITION_CHOICES)
    status = models.CharField(max_length=12, choices=[('AVAILABLE', 'Available'), ('UNAVAILABLE', 'Unavailable')], default='AVAILABLE')

    def __str__(self):
        return self.title

# upload to helper function    
def upload_to(instance, filename):
    product_id = instance.product_id or 'unsaved'
    return f'product_images/product_{product_id}/{filename}'
    
# product image model
class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to=upload_to)

class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    body = models.TextField()
    timestamp = models.DateTimeField(default=now)

    def __str__(self):
        return f"From {self.sender.username} to {self.receiver.username} about {self.product.title}"

# get default user helper function
def get_default_user():
    from .models import User
    return User.objects.first().id

# listing model
class UserExtraListings(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)  
    extra_listings = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.user} - {self.extra_listings} extra listings"
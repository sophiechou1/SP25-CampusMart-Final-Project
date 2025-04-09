from django.db import models

class User(models.Model):
    first_name = models.CharField(max_length=30, null=True, default="Default Name")
    username = models.CharField(max_length=200, unique=True)
    password = models.TextField()
    email = models.EmailField(max_length=200, unique=True)

    def __str__(self):
        return self.username
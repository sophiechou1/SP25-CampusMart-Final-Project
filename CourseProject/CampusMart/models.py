from django.db import models

class User(models.Model):
    username = models.CharField(max_length=200, unique=True)
    password = models.TextField()
    email = models.EmailField(max_length=200, unique=True)

    def __str__(self):
        return self.username
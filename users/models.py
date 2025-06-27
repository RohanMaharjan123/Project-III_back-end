from django.contrib.auth.models import AbstractUser
from django.db import models
# Create your models here.

# users/models.py


class User(AbstractUser):
    ROLE_CHOICES = (
        ('basic_user', 'Basic User'),
        ('premium_user', 'Premium User'),
        ('admin', 'Admin'),
    )
    # Add any other fields you had, like 'email' as unique
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, blank=True, null=True)
    
    # You can add other profile fields here or in a separate Profile model
    # e.g., phone, address, dob, gender from your SignupForm

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username'] # username can still be required for django-admin

    def __str__(self):
        return self.email

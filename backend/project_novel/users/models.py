from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    # user will have username, password, email, first_name, last_name, is_staff, is_active, date_joined, last_login
    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)

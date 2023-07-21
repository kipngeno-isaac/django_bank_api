from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    name=models.CharField(max_length=100)
    email = models.CharField(max_length=100, unique=True)
    address = models.CharField(max_length=100)
    balance = models.FloatField(default=0)
    password = models.CharField(max_length=250, default='')
    created = models.DateTimeField(auto_now_add=True)
    username = None

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS= []
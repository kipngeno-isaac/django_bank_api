from django.db import models

# Create your models here.
class User(models.Model):
    name=models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    account_number = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
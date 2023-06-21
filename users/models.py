from django.db import models

# Create your models here.
class User(models.Model):
    name=models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    balance = models.FloatField(default=0)
    created = models.DateTimeField(auto_now_add=True)
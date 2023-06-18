from django.db import models
from users.models import User

# Create your models here.
class Account(models.Model):
    user_id = models.IntegerField(default=0)
    debit = models.FloatField()
    credit = models.FloatField()
    balance = models.FloatField()
    created = models.DateTimeField(auto_now_add=True)

class Transaction(models.Model):
    user_id = models.IntegerField(default=0)
    Account_entry_id = models.IntegerField(default=0)
    description=models.CharField(max_length=100)
    transaction_type = models.CharField(max_length=100)
    amount = models.FloatField()
    created = models.DateTimeField(auto_now_add=True)


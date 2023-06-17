from django.db import models
from users.models import User

# Create your models here.
class Account(models.Model):
    user_id = models.ForeignKey(User, related_name='account_entries', on_delete=models.CASCADE)
    debit = models.FloatField()
    credit = models.FloatField()
    balance = models.FloatField()
    created = models.DateTimeField(auto_now_add=True)

class Transaction(models.Model):
    user_id = models.ForeignKey(User, related_name='transactions', on_delete=models.CASCADE)
    Account_entry_id = models.ForeignKey(Account, related_name='account_entry', on_delete=models.CASCADE)
    description=models.CharField(max_length=100)
    transaction_type = models.CharField(max_length=100)
    amount = models.FloatField()
    created = models.DateTimeField(auto_now_add=True)


from django.db import models

# Create your models here.
class Transaction(models.Model):
    user_id = models.IntegerField()
    description=models.CharField(max_length=100)
    transaction_type = models.CharField(max_length=100)
    amount = models.FloatField()
    balance = models.FloatField()
    created = models.DateTimeField(auto_now_add=True)


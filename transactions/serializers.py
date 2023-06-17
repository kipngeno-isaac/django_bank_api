from rest_framework import serializers 
from transactions.models import Transaction
from transactions.models import Account
 
 
class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ('id',
                  'description',
                  'transaction_type',
                  'amount',
                  'created')

class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = (
            'id',
            'user_id',
            'debit',
            'credit',
            'balance',
            'created'
        )
from django.shortcuts import render

from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser 
from rest_framework import status
 
from transactions.models import Transaction
from transactions.serializers import TransactionSerializer
from rest_framework.decorators import api_view
# Create your views here.
@api_view(['GET'])
def index(request):
    transactions = Transaction.objects.all()

    account_number = request.GET.get('account_number', None)
    if account_number is not None:
        transactions = transactions.filter(account_number__icontains=account_number)
    
    transactions_serializer = TransactionSerializer(transactions, many=True)
    return JsonResponse(transactions_serializer.data, safe=False)


@api_view(['POST'])
def deposit(request):
    deposit_data = JSONParser().parse(request)
    # todo: update balance
    transaction_data = {
        'user_id': deposit_data['user_id'],
        'description': "This {} has been deposited to you're account".format(deposit_data['amount']),
        'transaction_type': 'DEPOSIT',
        'amount': deposit_data['amount'],
        'balance': 0.0
    }
    transaction_serializer = TransactionSerializer(data = transaction_data)
    if transaction_serializer.is_valid():
        create_account_entry(transaction_data)
        transaction_serializer.save()
        return JsonResponse(transaction_serializer.data, status=status.HTTP_201_CREATED)
    return JsonResponse(transaction_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
def create_account_entry(transaction):
    # check db for the accounts last transaction
    print(transaction['transaction_type'])
    pass

def create_new_transaction():
    # use request details to update and create new transaction
    pass

def get_balance(user_id):
    transaction = Transaction.objects.filter(user_id=user_id).last()
    return transaction

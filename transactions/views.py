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
def store(request):
    transaction_data = JSONParser().parse(request)
    transaction_serializer = TransactionSerializer(data = transaction_data)
    if transaction_serializer.is_valid():
        transaction_serializer.save()
        return JsonResponse(transaction_serializer.data, status=status.HTTP_201_CREATED)
    return JsonResponse(transaction_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def get_latest_transaction():
    # check db for the accounts last transaction
    pass

def create_new_transaction():
    # use request details to update and create new transaction
    pass


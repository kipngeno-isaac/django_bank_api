from django.shortcuts import render

from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser 
from rest_framework import status
 
from transactions.models import Transaction
from transactions.serializers import TransactionSerializer
from rest_framework.decorators import api_view
from django.db import transaction
from users.models import User
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
    user_data = get_user(deposit_data['user_id'])
    print(user_data.balance)
    balance = user_data.balance
    new_balance = balance + deposit_data['amount']
    # todo: update balance
    transaction_data = {
        'user_id': deposit_data['user_id'],
        'description': "This {} has been deposited to you're account".format(deposit_data['amount']),
        'transaction_type': 'DEPOSIT',
        'amount': deposit_data['amount'],
        'balance': new_balance
    }

    transaction_serializer = TransactionSerializer(data = transaction_data)
    if transaction_serializer.is_valid():
        with transaction.atomic():
            transaction_serializer.save()
            user_data.balance = new_balance
            user_data.save()
            print(user_data.balance)
            return JsonResponse(transaction_serializer.data, status=status.HTTP_201_CREATED)
    return JsonResponse(transaction_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def withdraw(request):
    deposit_data = JSONParser().parse(request)
    user_data = get_user(deposit_data['user_id'])
    print(user_data.balance)
    balance = user_data.balance
    new_balance = balance - deposit_data['amount']
    if balance >= deposit_data['amount']:
        transaction_data = {
            'user_id': deposit_data['user_id'],
            'description': "This {} has been withdrawn from you're account".format(deposit_data['amount']),
            'transaction_type': 'WITHDRAW',
            'amount': deposit_data['amount'],
            'balance': new_balance
        }
        transaction_serializer = TransactionSerializer(data = transaction_data)
        if transaction_serializer.is_valid():
            with transaction.atomic():
                transaction_serializer.save()
                user_data.balance = new_balance
                user_data.save()
                print(user_data.balance)
                return JsonResponse(transaction_serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(transaction_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def transfer(request):
    transfer_data = JSONParser().parse(request)
    
    user_withdraw_data = {
        'user_id': transfer_data['user_id'],
        'description': "You have transfered {} to {}".format(transfer_data['amount'], transfer_data['receiver_id']),
        'transaction_type': 'WITHDRAW',
        'amount': transfer_data['amount'],
        'balance': 0.0
    }

    receiver_deposit_data = {
        'user_id': transfer_data['receiver_id'],
        'description': "You have received {} from {}".format(transfer_data['amount'], transfer_data['user_id']),
        'transaction_type': 'DEPOSIT',
        'amount': transfer_data['amount'],
        'balance': 0.0
    }

    with transaction.atomic():
        sender_data = TransactionSerializer(data=user_withdraw_data)
        if sender_data.is_valid():
            sender_data.save()
        receiver_data = TransactionSerializer(data=receiver_deposit_data)
        if receiver_data.is_valid():
            receiver_data.save()
        
        return JsonResponse(sender_data.data, status=status.HTTP_201_CREATED)


def create_new_transaction():
    # use request details to update and create new transaction
    pass

def get_balance(user_id):
    transaction = Transaction.objects.filter(user_id=user_id)
    return transaction.latest('created')

def get_user(user_id):
    return User.objects.get(pk=user_id)
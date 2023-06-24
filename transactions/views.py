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
    user_id = request.GET.get('user_id', None)
    print(user_id)
    if user_id is not None:
        transactions = transactions.filter(user_id__icontains=user_id)
    
    transactions_serializer = TransactionSerializer(transactions, many=True)
    return JsonResponse(transactions_serializer.data, safe=False)

@api_view(['GET'])
def get_transactions(request, user_id):

    transactions = Transaction.objects.filter(user_id = user_id)
    transactions_serializer = TransactionSerializer(transactions, many=True)
    return JsonResponse(transactions_serializer.data, safe=False)

@api_view(['POST'])
def deposit(request):
    deposit_data = JSONParser().parse(request)
    user_data = get_user(deposit_data['user_id'])
    balance = user_data.balance
    new_balance = balance + deposit_data['amount']
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
    balance = user_data.balance
    new_balance = balance - deposit_data['amount']
    if deposit_data['amount'] > balance:
        return JsonResponse("Withdrawal amount exceeds your balance", status=status.HTTP_400_BAD_REQUEST, safe=False)

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
    sender = get_user(transfer_data['user_id'])
    receiver = get_user(transfer_data['receiver_id'])
    sender_balance = sender.balance
    if sender_balance < transfer_data['amount']:
        return JsonResponse("You're transfer amount exceeds your balance", status=status.HTTP_400_BAD_REQUEST, safe=False)

    sender_new_balance = sender_balance - transfer_data['amount']
    user_withdraw_data = {
        'user_id': transfer_data['user_id'],
        'description': "You have transfered {} to {}".format(transfer_data['amount'], receiver.name),
        'transaction_type': 'WITHDRAW',
        'amount': transfer_data['amount'],
        'balance': sender_new_balance
    }
    receiver_balance = receiver.balance
    receiver_new_balance = receiver_balance + transfer_data['amount']
    receiver_deposit_data = {
        'user_id': transfer_data['receiver_id'],
        'description': "You have received {} from {}".format(transfer_data['amount'], transfer_data['user_id']),
        'transaction_type': 'DEPOSIT',
        'amount': transfer_data['amount'],
        'balance': receiver_new_balance
    }

    with transaction.atomic():
        sender_data = TransactionSerializer(data=user_withdraw_data)
        if sender_data.is_valid():
            sender_data.save()
            sender.balance = sender_new_balance
            sender.save()
        receiver_data = TransactionSerializer(data=receiver_deposit_data)
        if receiver_data.is_valid():
            receiver_data.save()
            receiver.balance = receiver_new_balance
            receiver.save()
        
        return JsonResponse(sender_data.data, status=status.HTTP_201_CREATED)

def get_user(user_id):
    return User.objects.get(pk=user_id)
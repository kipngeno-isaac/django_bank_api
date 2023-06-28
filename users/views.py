from django.shortcuts import render

from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser 
from rest_framework import status
 
from users.models import User
from users.serializers import UserSerializer
from users.serializers import UserRegistrationSerializer
from rest_framework.decorators import api_view
from rest_framework.authtoken.models import Token
# Create your views here.
@api_view(['GET'])
def user_list(request):
    users = User.objects.all()
    name = request.GET.get('name', None)
    if name is not None:
        users = users.filter(name__icontains=name)
    
    users_serializer = UserSerializer(users, many=True)
    return JsonResponse(users_serializer.data, safe=False)

@api_view(['POST'])
def user_create(request):
    user_data = JSONParser().parse(request)
    user_serializer = UserSerializer(data=user_data)
    if user_serializer.is_valid():
        user_serializer.save()
        return JsonResponse(user_serializer.data, status=status.HTTP_201_CREATED) 
    return JsonResponse(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def register_user(request):
    userSerializer = UserRegistrationSerializer(data=request.data)
    data = {}

    if userSerializer.is_valid():
        user = userSerializer.save()

        data['message'] = 'User registered successfully'
        data['name'] = user.name
        data['email'] = user.email

        token= Token.objects.get(user=user).key
        data['token'] = token

    else:
        data = userSerializer.errors

    return JsonResponse(data)
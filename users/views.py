from django.shortcuts import render

from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser 
from rest_framework import status
 
from users.models import User
from users.serializers import UserSerializer
from rest_framework.decorators import api_view
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

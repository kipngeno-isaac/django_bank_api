from rest_framework import serializers, validators 
# from users.models import User
from .models import User

 
class UserSerializer(serializers.ModelSerializer):
    balance = serializers.FloatField(required=False)
    class Meta:
        model = User
        fields = ('id',
                  'name',
                  'email',
                  'password',
                  'address',
                  'balance')
        etra_kwargs = {
            'password': {'write_only': True},
            'balance':{'read_only': True}
        }
        
    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance
        
class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'first_name', 'last_name']
        etra_kwargs = {
            'password': {'write_only': True},
            'email': {
                'required': True,
                'validators': [
                    validators.UniqueValidator(
                        User.objects.all(), "A user with this email already exist"
                    )
                ]
            }
        }

    def create(self, validated_data):
        user = User.objects.create(
            username = validated_data.get('username'),
            password = validated_data.get('password'),
            email=validated_data.get('email'),
            first_name=validated_data.get('first_name'),
            last_name = validated_data.get('last_name')
        )
        return user


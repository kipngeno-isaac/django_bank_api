from rest_framework import serializers 
from users.models import User
 
 
class UserSerializer(serializers.ModelSerializer):
    balance = serializers.FloatField(required=False)
    class Meta:
        model = User
        fields = ('id',
                  'name',
                  'email',
                  'address',
                  'balance',
                  'created')

        def create(self, validated_data):
            # Remove the optional_field from validated_data
            validated_data.pop('balance', None)
            return super().create(validated_data)

        def update(self, instance, validated_data):
            # Remove the optional_field from validated_data
            validated_data.pop('balance', None)

            # Call the parent's update() method to save the object
            return super().update(instance, validated_data)
        
class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(style={'input_type':'password'},write_only=True)
    class Meta:
        model = User
        fields = ['name', 'email', 'address', 'password']
        etra_kwargs = {
            'password': {'write_only': True}
        }

    def save(self):
        password = self.validated_data['password']

        if User.objects.filter(email = self.validated_data['email']).exists():
            raise serializers.ValidationError({"Error":"Email already exists"})
        
        user = User(name=self.validated_data['name'], email=self.validated_data['email'], address= self.validated_data['address'])
        user.set_password(password)
        user.save()

        return user


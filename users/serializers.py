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
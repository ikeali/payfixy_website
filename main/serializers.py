from rest_framework import serializers
from .models import User
from django_countries import countries



# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         exclude = ["password", "id", 'is_superuser', 'is_staff']
        


class UserSerializer(serializers.ModelSerializer):
    pk = serializers.UUIDField(source='uuid')

    class Meta:
        model = User
        exclude = ["password", "is_superuser", "is_staff"] 

    def to_representation(self, instance):
        # Customize the response to include `uuid` as `pk`
        representation = super().to_representation(instance)
        representation['pk'] = instance.uuid  # Override pk field with uuid
        return representation


class SignUpSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    country = serializers.CharField()


    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'country', 'business_type', 'business_name', 'password']

    
    def create(self, validated_data):
        password = validated_data.pop('password')
        merchant =User(**validated_data)
        merchant.set_password(password)  
        merchant.save()
        return merchant

    

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()
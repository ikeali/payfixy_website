from rest_framework import serializers
from .models import User
from kyc.serializers import KYCSerializer
from django_countries import countries



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        # exclude = ["password", "id", 'is_superuser', 'is_staff']
        fields = '__all__'


# class UserSerializer(serializers.ModelSerializer):
#     # uuid = serializers.UUIDField(source='uuid', read_only=True)  # The unique identifier is UUID
#     uuid = serializers.UUIDField(read_only=True)  # The unique identifier is UUID
#     kyc = KYCSerializer(read_only=True)  # Serialize KYC data
    
#     class Meta:
#         model = User
#         fields = '__all__'


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
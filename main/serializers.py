from rest_framework import serializers
from .models import User
from django_countries import countries


class SignUpSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    country = serializers.CharField()


    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'country', 'business_type', 'business_name', 'password']




    # def validate_country(self, value):
    #     # Convert three-letter codes to two-letter codes if needed
    #     if len(value) == 3:
    #         for code, name in countries:
    #             if countries.alpha3(code) == value:
    #                 return code  # returns the two-letter code
    #         raise serializers.ValidationError(f"{value} is not a valid ISO country code.")
    #     return value
    
    def create(self, validated_data):
        password = validated_data.pop('password')
        merchant =User(**validated_data)
        merchant.set_password(password)  
        merchant.save()
        return merchant

    

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()
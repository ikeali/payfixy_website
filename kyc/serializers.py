from rest_framework import serializers
from .models import *

class BusinessDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusinessDetails
        fields = '__all__'
        read_only_fields = ['id']


class BusinessDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusinessDocument
        fields = '__all__'
        read_only_fields = ['id']


# class BankAccountSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = BankAccount
#         fields = '__all__'
#         read_only_fields = ['id', 'account_number', 'bank_name']


class BusinessOwnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusinessOwner
        fields = '__all__'
        read_only_fields = ['id']


    def create(self, validated_data):
        """
        Create a BusinessOwner instance.
        """
        # If needed, perform any custom creation logic here
        return super().create(validated_data)


    def update(self, instance, validated_data):
        """
        Update an existing BusinessOwner instance.
        """
        # If needed, perform any custom update logic here
        return super().update(instance, validated_data)


class KYCSerializer(serializers.ModelSerializer):
    class Meta:
        model = KYC
        fields = ['merchant', 'status']
        read_only_fields = ['id']
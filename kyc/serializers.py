from rest_framework import serializers
from .models import *

class BusinessDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusinessDetails
        fields = '__all__'
        read_only_fields = ['merchant', 'created_at', 'updated_at']


class BusinessDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusinessDocument
        fields = '__all__'
        read_only_fields = ['merchant', 'uploaded_at']


class BusinessOwnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusinessOwner
        fields = '__all__'





class KYCSummarySerializer(serializers.ModelSerializer):
    business_details = BusinessDetailsSerializer(source="merchant.businessdetails", read_only=True)
    business_documents = BusinessDocumentSerializer(source="merchant.businessdocument", read_only=True)
    # bank_account = BankAccountSerializer(source="merchant.bankaccount", read_only=True)
    business_owner = BusinessOwnerSerializer()
    kyc_status = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ['business_details', 'business_documents', 'business_owner', 'kyc_status']
    
    def get_kyc_status(self, obj):
        status = KYCStatus.objects.get(merchant=obj)
        return {
            "completed_business_details": status.completed_business_details,
            "completed_business_documents": status.completed_business_documents,
            # "completed_bank_account": status.completed_bank_account,
            "overall_completed": all([
                status.completed_business_details,
                status.completed_business_documents,
                status.completed_bank_account,
            ])
        }

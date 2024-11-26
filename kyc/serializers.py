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

class BankAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = BankAccount
        fields = '__all__'
        read_only_fields = ['merchant', 'account_number', 'bank_name']




class BusinessOwnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusinessOwner
        # fields = [
        #     'role', 'full_name', 'email_address', 'phone_number', 'share_ownership',
        #     'Bvn', 'home_address', 'location', 'government_id', 'government_id_number', 'date_of_birth'
           
        # ]
        fields = '__all__'

    # def validate(self, data):
    #     """
    #     Override validate method to check if the BVN and Date of Birth match.
    #     """
    #     bvn = data.get('Bvn')
    #     dob = data.get('date_of_birth')
    #     full_name = data.get('full_name')

    #     if bvn and dob:
    #         # You can use the model method for BVN and DOB verification
    #         business_owner = BusinessOwner(
    #             full_name=full_name,
    #             Bvn=bvn,
    #             date_of_birth=dob
    #         )

    #         # Now use the verify method defined in your BusinessOwner model
    #         try:
    #             business_owner.verify_bvn_and_dob()
    #         except serializers.ValidationError as e:
    #             raise e  # Reraise the validation error

    #     return data

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

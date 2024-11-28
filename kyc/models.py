from django.db import models
from django.core.exceptions import ValidationError
from main.models import User
from utility.encryption import encrypt_data, decrypt_data
from utility.validator import validate_file_type
import requests
from .tasks import verify_bvn_and_dob

from django.core.validators import RegexValidator, EmailValidator

from decouple import config


class KYC(models.Model):

    STATUS =[
        ('in_progress', 'In progress'),
        ('completed', 'Completed')
    ]
    merchant = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=50, choices=STATUS, null=False, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

   


class BusinessDetails(models.Model): 
    # merchant = models.OneToOneField(User, on_delete=models.CASCADE)
    kyc = models.ForeignKey(KYC, related_name='business_details', on_delete=models.CASCADE, default=None)
    business_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20, validators=[RegexValidator(regex=r'^\+?1?\d{9,15}$',
                message="Phone number must be in the format: '+999999999'. Up to 15 digits allowed."
            )
        ]
    )    
    business_location = models.CharField(max_length=100)
    busienss_description = models.TextField(blank=True, null=True)
    industry = models.CharField(max_length=50)
    business_address = models.CharField(max_length=255)
    expected_transaction_volume = models.DecimalField(max_digits=15, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class BusinessDocument(models.Model):
    # merchant = models.ForeignKey(User, on_delete=models.CASCADE, related_name='business_documents')
    kyc = models.ForeignKey(KYC, related_name='business_documents', on_delete=models.CASCADE,default=None)
    cac_reg_number= models.CharField(max_length=100)
    cac_document = models.FileField(upload_to='kyc_documents/', validators=[validate_file_type])
    memorandum_and_article_association = models.FileField(upload_to='kyc_documents/')
    proof_of_address = models.BooleanField(default=False)
    uploaded_at = models.DateTimeField(auto_now_add=True)



    def save(self, *args, **kwargs):
        if self.cac_reg_number:
            self.cac_reg_number = encrypt_data(self.cac_reg_number)
        super().save(*args, **kwargs)

    @property
    def decrypted_cac_reg_number(self):
        return decrypt_data(self.cac_reg_number)

 
# class BankAccount(models.Model):
#     # Merchant = models.ForeignKey(User, on_delete=models.CASCADE)
#     kyc = models.ForeignKey(KYC, related_name='bank_account', on_delete=models.CASCADE)
#     bank_name = models.CharField(max_length=50)
#     account_number = models.CharField(max_length=10)


    def save(self, *args, **kwargs):
        if self.account_number:
            self.account_number = encrypt_data(self.account_number)
        super().save(*args, **kwargs)

    @property
    def decrypted_cac_reg_number(self):
        return decrypt_data(self.account_number)
    

class BusinessOwner(models.Model):
    ROLE_TYPES= [
        ('owner', 'Owner')
        # ('', ''),
    ]


    SHARE_OWNERSHIP_CHOICES= [
        ('director', 'Director'),
        ('ceo', 'CEO'),
    ]

    GOVERNMENT_ID= [
        ('voters card', 'Voters card'),
        ('drivers license', 'Drivers license'),
        ('international passport', 'International Passport'),
        ('national id', 'National id')
    ]
    # merchant = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    kyc = models.ForeignKey(KYC, related_name='business_owner', on_delete=models.CASCADE,default=None)
    role = models.CharField(max_length=50, choices = ROLE_TYPES)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100, default=None)
    email_address = models.EmailField(validators=[EmailValidator()])
    phone_number = models.CharField(
    max_length=20,
    validators=[
        RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be in the format: '+999999999'. Up to 15 digits allowed.")
    ]
    )
    share_ownership = models.CharField(max_length=100, choices=SHARE_OWNERSHIP_CHOICES)
    bvn = models.CharField(max_length=255)
    home_address = models.CharField(max_length=100)
    location= models.CharField(max_length=100)
    government_id = models.CharField(max_length=100, choices=GOVERNMENT_ID)
    government_id_number = models.CharField(max_length=100)
    # upload_id = models.FileField(upload_to='kyc_documents/')
    date_of_birth = models.DateTimeField()


    def save(self, *args, **kwargs):
        # Encrypt sensitive fields only when they are updated
        if self.pk:
            original = BusinessOwner.objects.get(pk=self.pk)
            if self.bvn != original.bvn:
                self.bvn = encrypt_data(self.bvn)
            if self.government_id_number != original.government_id_number:
                self.government_id_number = encrypt_data(self.government_id_number)
        else:
            self.bvn = encrypt_data(self.bvn)
            self.government_id_number = encrypt_data(self.government_id_number)
        super().save(*args, **kwargs)

    @property
    def decrypted_bvn(self):
        return decrypt_data(self.bvn)

    @property
    def decrypted_government_id_number(self):
        return decrypt_data(self.government_id_number)


    def enqueue_bvn_verification(self):
        result = verify_bvn_and_dob.delay(self.bvn, self.first_name, self.last_name, self.date_of_birth)
        return result

    # def verify_bvn_and_dob(self):
       
    #     url = f"https://api.qoreid.com/v1/ng/identities/bvn-premium/{22182106897}"
    #     headers = {
    #         "Authorization": f"Bearer {config('COREID_TOKEN')}",
    #         "Content-Type": "application/json",
    #     }

    
    #     payload = {
    #         "firstname": self.first_name,
    #         "lastname": self.last_name
    #     }

    #     try:
    #         response = requests.post(url, headers=headers, json=payload)
    #         response.raise_for_status() 

    #         data = response.json()

    #         if data.get("status") != "verified":
    #             raise ValidationError("The BVN verification failed.")

    #         # If the BVN is valid, verify the Date of Birth
    #         verify_dob = data.get("data", {}).get("dob")
    #         if verify_dob != self.date_of_birth.strftime('%d-%m-%Y'):
    #             raise ValidationError("The BVN and Date of Birth do not match.")

    #         return True
    #     except requests.exceptions.RequestException as e:
    #         raise ValidationError(f"An error occurred while verifying BVN: {str(e)}")


    # def clean(self):
    #     """
    #     Perform model validation before saving the instance.
    #     """
    #     super().clean()
    #     self.verify_bvn_and_dob()

    # def save(self, *args, **kwargs):
    #     # self.full_clean()  # This calls `clean()` method
    #     super().save(*args, **kwargs)
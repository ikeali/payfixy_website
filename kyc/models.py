from django.db import models
from main.models import User
from utility.encryption import encrypt_data, decrypt_data


class KYCStatus(models.Model):
    merchant = models.OneToOneField(User, on_delete=models.CASCADE)
    completed_business_details = models.BooleanField(default=False)
    completed_business_documents = models.BooleanField(default=False)
    completed_bank_account = models.BooleanField(default=False)
    completed_business_owner = models.BooleanField(default=False)

    def __str__(self):
        return f"KYC status for {self.merchant.email}"



class BusinessDetails(models.Model): 
    merchant = models.OneToOneField(User, on_delete=models.CASCADE)
    business_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)
    business_location = models.CharField(max_length=100)
    busienss_description = models.TextField(blank=True, null=True)
    industry = models.CharField(max_length=50)
    business_address = models.CharField(max_length=255)
    expected_transaction_volume = models.DecimalField(max_digits=15, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class BusinessDocument(models.Model):
    merchant = models.ForeignKey(User, on_delete=models.CASCADE, related_name='business_documents')
    cac_reg_number= models.CharField(max_length=50)
    cac_document = models.FileField(upload_to='kyc_documents/')
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
#     Merchant = models.ForeignKey(Merchant, on_delete=models.CASCADE)
#     bank_name = models.CharField(max_length=50)
#     accoun_number = models.CharField(max_length=10)

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

    role = models.CharField(max_length=50, choices = ROLE_TYPES)
    full_name = models.CharField(max_length=100)
    email_address =models.CharField(max_length=100)
    phone_number = models.CharField(max_length=50)
    share_ownership = models.CharField(max_length=100, choices=SHARE_OWNERSHIP_CHOICES)
    Bvn = models.CharField(max_length=11)
    home_address = models.CharField(max_length=100)
    location= models.CharField(max_length=100)
    government_id = models.CharField(max_length=100, choices=GOVERNMENT_ID)
    government_id_number = models.CharField(max_length=100)
    upload_id = models.FileField(upload_to='kyc_documents/')
    date_of_birth = models.DateTimeField(auto_now_add=True)
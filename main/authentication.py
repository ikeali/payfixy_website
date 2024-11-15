# # authentication.py
# from django.contrib.auth.backends import ModelBackend
# from .models import Merchant

# class EmailAuthBackend(ModelBackend):
#     def authenticate(self, request, email=None, password=None, **kwargs):
#         try:
#             merchant = Merchant.objects.get(email=email)
#             if merchant.check_password(password):
#                 return merchant
#         except Merchant.DoesNotExist:
#             return None

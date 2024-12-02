import re
from rest_framework_simplejwt.tokens import RefreshToken
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth import login
from django.core.mail import send_mail
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework.permissions import AllowAny
from .serializers import *
from .models import *
from decouple import config
from django.http import HttpResponse
from django.utils.timezone import now, timedelta
import random




def index(request):
    return HttpResponse("Hello, world. This is the root page!")

# Simple homepage view
def homepage(request):
    return Response("Welcome to PayFixy!")


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
from django.core.mail import send_mail
from datetime import timedelta
from django.utils.timezone import now
from decouple import config
import random
from .models import OTP
from .serializers import SignUpSerializer  


class SignUpView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        if serializer.is_valid():
            try:
                user = serializer.save(is_active=False, is_email_verified=False)

                # Generate OTP
                otp_code = f"{random.randint(100000, 999999)}"
                OTP.objects.create(
                    email=user.email,
                    code=otp_code,
                    created_at=now(),
                    expires_at=now() + timedelta(minutes=10),
                )

                send_mail(
                    "Email Verification",
                    f"Your OTP is: {otp_code}",
                    config("EMAIL_HOST_USER"),
                    [user.email],
                    fail_silently=False,
                )

                return Response(
                    {
                        "status_code": status.HTTP_201_CREATED,
                        "message": "Merchant created successfully. Check your email for OTP verification."
                    },
                    status=status.HTTP_201_CREATED,
                )
            except Exception as e:
                return Response(
                    {
                        "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                        "error": "An error occurred while processing your request.",
                        "details": str(e),
                    },
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )

        return Response(
            {
                "status_code": status.HTTP_400_BAD_REQUEST,
                "error": "Invalid data provided.",
                "details": serializer.errors,
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    


class VerifyEmailView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        otp_code = request.data.get('otp')

        if not email or not otp_code:
            return Response({
                'status_code': status.HTTP_400_BAD_REQUEST,
                "error": "Email and OTP are required."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            # Fetch the OTP object
            otp = OTP.objects.get(email=email, code=otp_code)
            
            # Check if the OTP has expired
            if otp.has_expired():
                return Response({
                    'status_code': status.HTTP_400_BAD_REQUEST,
                    "error": "OTP has expired."
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            otp.is_verified = True
            otp.save()

            # Fetch the User object
            user = User.objects.get(email=email)
            user.is_email_verified = True
            user.is_active = True 

            user.save()

            return Response({
                'status_code': status.HTTP_200_OK,
                "message": "Email verified successfully."
                },
                status=status.HTTP_200_OK
            )

        except OTP.DoesNotExist:
            return Response({
                'status_code': status.HTTP_400_BAD_REQUEST,
                "error": "Invalid OTP or email."
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        except User.DoesNotExist:
            return Response({
                'status_code': status.HTTP_404_NOT_FOUND,
                "error": "User with this email does not exist."
                },
                status=status.HTTP_404_NOT_FOUND    
            )




# class LoginView(APIView):
#     permission_classes = [AllowAny]

#     def post(self, request, *args, **kwargs):
#         email = request.data.get('email')
#         password = request.data.get('password')

#         # Check if email and password are provided
#         if not email or not password:
#             return Response(
#                 {
#                     'status_code': status.HTTP_400_BAD_REQUEST,
#                     'error': 'Email and password are required.'
#                 },
#                 status=status.HTTP_400_BAD_REQUEST
#             )

#         # Authenticate the user
#         user = authenticate(email=email, password=password)
#         if not user:
#             return Response(
#                 {
#                     'status_code': status.HTTP_401_UNAUTHORIZED,
#                     'error': 'Invalid credentials'
#                 },
#                 status=status.HTTP_401_UNAUTHORIZED
#             )
    
#         # Generate OTP
#         otp_code = f"{random.randint(100000, 999999)}"
#         OTP.objects.create(
#             email=email,
#             code=otp_code,
#             created_at=now(),
#             expires_at=now() + timedelta(minutes=10),
#         )

#         user = User.objects.get(email=email)
#         refresh = RefreshToken.for_user(user)

#         return Response(
#             {
#                 'status_code': status.HTTP_200_OK,
#                 'message': 'Login successful.',
#                 'access_token': str(refresh.access_token),
#                 'refresh_token': str(refresh),
#             },
#             status=status.HTTP_200_OK
#         )



class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')

        # Check if email and password are provided
        if not email or not password:
            return Response(
                {
                    'status_code': status.HTTP_400_BAD_REQUEST,
                    'error': 'Email and password are required.'
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        # Authenticate the user
        user = authenticate(email=email, password=password)
        if not user:
            return Response(
                {
                    'status_code': status.HTTP_401_UNAUTHORIZED,
                    'error': 'Invalid credentials'
                },
                status=status.HTTP_401_UNAUTHORIZED
            )
    
        # Generate OTP
        otp_code = f"{random.randint(100000, 999999)}"
        OTP.objects.create(
            email=email,
            code=otp_code,
            created_at=now(),
            expires_at=now() + timedelta(minutes=10),
        )

        # Generate tokens
        refresh = RefreshToken.for_user(user)

        # Serialize user data
        user_data = UserSerializer(user).data

        return Response(
            {
                'status_code': status.HTTP_200_OK,
                'message': 'Login successful.',
                'access_token': str(refresh.access_token),
                'refresh_token': str(refresh),
                'user': user_data,  # Include serialized user data
            },
            status=status.HTTP_200_OK
        )


# class LoginView(APIView):
#     permission_classes = [AllowAny]

#     def post(self, request, *args, **kwargs):
#         email = request.data.get('email')
#         password = request.data.get('password')

#         # Check if email and password are provided
#         if not email or not password:
#             return Response(
#                 {
#                     'status_code': status.HTTP_400_BAD_REQUEST,
#                     'error': 'Email and password are required.'
#                 },
#                 status=status.HTTP_400_BAD_REQUEST
#             )

#         # Authenticate the user
#         user = authenticate(email=email, password=password)
#         if not user:
#             return Response(
#                 {
#                     'status_code': status.HTTP_401_UNAUTHORIZED,
#                     'error': 'Invalid credentials'
#                 },
#                 status=status.HTTP_401_UNAUTHORIZED
#             )
    
#         # Generate OTP
#         otp_code = f"{random.randint(100000, 999999)}"
#         OTP.objects.create(
#             email=email,
#             code=otp_code,
#             created_at=now(),
#             expires_at=now() + timedelta(minutes=10),
#         )

#         # Send OTP via email
#         try:
#             send_mail(
#                 'Login OTP',
#                 f'Your OTP for login is: {otp_code}',
#                 config('EMAIL_HOST_USER'),
#                 [user.email],
#                 fail_silently=False,
#             )
#         except Exception as e:
#             return Response(
#                 {
#                     'status_code': status.HTTP_500_INTERNAL_SERVER_ERROR,
#                     'error': 'Failed to send OTP',
#                     'details': str(e)
#                 },
#                 status=status.HTTP_500_INTERNAL_SERVER_ERROR
#             )

#         return Response(
#             {
#                 'status_code': status.HTTP_200_OK,
#                 'message': 'OTP sent to your email. Please verify to complete login.'
#             },
#             status=status.HTTP_200_OK
#         )


# class LoginConfirmView(APIView):
#     permission_classes = [AllowAny]

#     def post(self, request, *args, **kwargs):
#         email = request.data.get('email')
#         otp_code = request.data.get('otp')

#         if not email or not otp_code:
#             return Response(
#                 {
#                     'status_code': status.HTTP_400_BAD_REQUEST,
#                     'error': 'Email and OTP are required.'
#                 },
#                 status=status.HTTP_400_BAD_REQUEST
#             )

#         try:
#             otp = OTP.objects.get(email=email, code=otp_code)

#             # Check if the OTP has expired
#             if otp.has_expired():
#                 return Response(
#                     {
#                         'status_code': status.HTTP_400_BAD_REQUEST,
#                         'error': 'OTP has expired.'
#                     },
#                     status=status.HTTP_400_BAD_REQUEST
#                 )

#             otp.is_verified = True
#             otp.save()

#             # Retrieve the user and generate tokens
#             user = User.objects.get(email=email)
#             refresh = RefreshToken.for_user(user)

#             return Response(
#                 {
#                     'status_code': status.HTTP_200_OK,
#                     'message': 'Login successful.',
#                     'access_token': str(refresh.access_token),
#                     'refresh_token': str(refresh),
#                 },
#                 status=status.HTTP_200_OK
#             )

#         except OTP.DoesNotExist:
#             return Response(
#                 {
#                     'status_code': status.HTTP_400_BAD_REQUEST,
#                     'error': 'Invalid OTP or email.'
#                 },
#                 status=status.HTTP_400_BAD_REQUEST
#             )
#         except User.DoesNotExist:
#             return Response(
#                 {
#                     'status_code': status.HTTP_404_NOT_FOUND,
#                     'error': 'User not found.'
#                 },
#                 status=status.HTTP_404_NOT_FOUND
#             )


class ForgotPasswordView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        email = request.data.get('email')

        try:
            merchant = User.objects.get(email=email)
            print(merchant)

            otp_code = f"{random.randint(100000, 999999)}"
            OTP.objects.create(
            email=email,
            code=otp_code,
            created_at=now(),
            expires_at=now() + timedelta(minutes=10),
        )

            send_mail(
                'Reset Your Password',
                f'Your OTP for reset password is: {otp_code}',
                config('EMAIL_HOST_USER'),
                [merchant.email],
                fail_silently=False,
            )

            return Response(
                {
                    'status_code': status.HTTP_200_OK,
                    'message': 'Password otp sent to email.'
                },
                status=status.HTTP_200_OK
            )
        except User.DoesNotExist:
   
            return Response(
                {
                    'status_code': status.HTTP_404_NOT_FOUND,
                    'error': 'User with this email does not exist.'
                },
                status=status.HTTP_404_NOT_FOUND
            )



class PasswordResetConfirmView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        otp_code = request.data.get('otp')
        new_password = request.data.get('password')

        try:
            # Validate OTP
            otp = OTP.objects.get(email=email, code=otp_code)

            if otp.has_expired():
                return Response({
                    'status_code': status.HTTP_400_BAD_REQUEST,
                    'error': 'OTP has expired.'
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

            if not otp.is_verified:
                otp.is_verified = True
                otp.save()

            # Validate password
            if not self.is_valid_password(new_password):
                return Response({
                    'status_code': status.HTTP_400_BAD_REQUEST,
                    'error': ('Password must be at least 8 characters long, include uppercase and lowercase letters, '
                              'a number, and a special character.')
                }, 
                status=status.HTTP_400_BAD_REQUEST
                )

            # Reset password
            user = User.objects.get(email=email)
            user.set_password(new_password)
            user.save()

            return Response({
                'status_code': status.HTTP_200_OK,
                'message': 'Password reset successful.'
                },
                status=status.HTTP_200_OK
            )

        except OTP.DoesNotExist:
            return Response({
                'status_code': status.HTTP_404_NOT_FOUND,
                'error': 'Invalid OTP or email.'
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        except User.DoesNotExist:
            return Response({
                'status_code': status.HTTP_404_NOT_FOUND,
                'error': 'User not found.'
                },
                status=status.HTTP_404_NOT_FOUND
            )

    def is_valid_password(self, password):
        """
        Validates the password with the following requirements:
        - Minimum 8 characters
        - At least one uppercase letter
        - At least one lowercase letter
        - At least one digit
        - At least one special character
        """
        if (len(password) < 8 or
            not re.search(r"[A-Z]", password) or       # Uppercase letter
            not re.search(r"[a-z]", password) or       # Lowercase letter
            not re.search(r"[0-9]", password) or       # Digit
            not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password)):  # Special character
            return False
        return True
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





# Simple homepage view
def homepage(request):
    return Response("Welcome to PayFixy!")


class SignUpView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Merchant created successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        print(email)
        password = request.data.get('password')
        print(password)

        # Authenticate the merchant
        merchant = authenticate(email=email, password=password)
        print(merchant)
        if not merchant:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


        # Create JWT token for the merchant
        refresh = RefreshToken.for_user(merchant)
        access_token = refresh.access_token


        # Generate a login confirmation link
        uid = urlsafe_base64_encode(force_bytes(merchant.pk))
        login_link = request.build_absolute_uri(
            reverse('login-confirm', kwargs={'uidb64': uid})
        )

        # Send the confirmation link via email
        try:
            send_mail(
                'Confirm Your Login',
                f'Please click the following link to confirm your login:\n\n{login_link}',
                config('EMAIL_HOST_USER'),
                [merchant.email],
                fail_silently=False,
            )
        except Exception as e:
            return Response({'error': 'Failed to send confirmation link', 'details': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({
            'message': 'Login successful',
            'access_token': str(access_token),
            'refresh_token': str(refresh),
        }, status=status.HTTP_200_OK)
    


class LoginConfirmView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, uidb64, *args, **kwargs):
        try:
            # Decode the merchant ID from the URL
            uid = urlsafe_base64_decode(uidb64).decode()
            merchant = User.objects.get(pk=uid)
            
            login(request, merchant)

            return Response({
                'message': 'Login confirmed. You are now logged in.',
                'user_id': merchant.id
            }, status=status.HTTP_200_OK)
        
        except (User.DoesNotExist, ValueError, TypeError, OverflowError):
            return Response({'error': 'Invalid login link'}, status=status.HTTP_400_BAD_REQUEST)



class ForgotPasswordView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        email = request.data.get('email')

        try:
            merchant = User.objects.get(email=email)
            print(merchant)

            # Encode the user ID to be used in the reset link
            uid = urlsafe_base64_encode(str(merchant.pk).encode()) 
            # Build the password reset link
            reset_link = self.build_reset_link(request, uid)

            send_mail(
                'Reset Your Password',
                f'Please click the following link to reset your password: {reset_link}',
                config('EMAIL_HOST_USER'),
                [merchant.email],
                fail_silently=False,
            )

            return Response({'message': 'Password reset link sent to email.'}, status=status.HTTP_200_OK)

        except User.DoesNotExist:
   
            return Response({'error': 'User with this email does not exist.'}, status=status.HTTP_404_NOT_FOUND)



    def build_reset_link(self, request, uidb64):
        """
        This method builds the reset password URL with the user ID.
        """
        reset_url = reverse('password-reset-confirm', kwargs={'uidb64': uidb64})
        
        # Build the absolute URL to the reset page
        return request.build_absolute_uri(reset_url)



class PasswordResetConfirmView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, uidb64, *args, **kwargs):
        try:
            # Decode the user ID
            uid = urlsafe_base64_decode(uidb64).decode()
            merchant = User.objects.get(pk=uid)

            # Proceed to show a form or page where the user can reset their password
            return Response({'message': 'Please submit your new password.'}, status=status.HTTP_200_OK)

        except User.DoesNotExist:
            return Response({'error': 'Invalid reset link'}, status=status.HTTP_400_BAD_REQUEST)
        

    def post(self, request, uidb64, *args, **kwargs):
        try:
            # Decode the user ID
            uid = urlsafe_base64_decode(uidb64).decode()
            merchant = User.objects.get(pk=uid)

            # Get the new password from the request
            new_password = request.data.get('password')

            # Password validation
            if not self.is_valid_password(new_password):
                return Response({'error': 'Password must be at least 8 characters long, include uppercase and lowercase letters, a number, and a special character.'},
                                status=status.HTTP_400_BAD_REQUEST)

            # Set the new password
            merchant.set_password(new_password)
            merchant.save()

            return Response({'message': 'Password reset successful'}, status=status.HTTP_200_OK)

        except User.DoesNotExist:
            return Response({'error': 'Invalid reset link'}, status=status.HTTP_400_BAD_REQUEST)


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
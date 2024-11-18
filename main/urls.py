from django.urls import path
from .views import *



urlpatterns = [
    path('', homepage, name='homepage'),  # Add this line for root URL
    path('onboarding/', SignUpView.as_view(), name='onboarding'),
    path('login/', LoginView.as_view(), name='login'),
    path('login-confirm/<uidb64>/', LoginConfirmView.as_view(), name='login-confirm'),
    path('reset-password/', ForgotPasswordView.as_view(), name='reset-password'),
    path('password-reset-confirm/<uidb64>/', PasswordResetConfirmView.as_view(), name='password-reset-confirm'),
]


from django.urls import path
from .views import *



urlpatterns = [
    path('', homepage, name='homepage'),
    path('onboarding/', SignUpView.as_view(), name='onboarding'),
    path('verify_email/', VerifyEmailView.as_view(), name='verufy_email'),
    path('login/', LoginView.as_view(), name='login'),
    # path('login-confirm/', LoginConfirmView.as_view(), name='login-confirm'),
    path('reset-password/', ForgotPasswordView.as_view(), name='reset-password'),
    path('password-reset-confirm/', PasswordResetConfirmView.as_view(), name='password-reset-confirm'),
]


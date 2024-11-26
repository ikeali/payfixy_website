import random
import jwt
from datetime import datetime, timedelta
from rest_framework.exceptions import AuthenticationFailed
from decouple import config
from main.models import *



def generate_otp(email):
    otp = random.randint(100000, 999999)  # Generate a 6-digit OTP
    # Save the OTP in your database, associated with the user's email (simplified here)
    # Store with an expiration time of 5 minutes, for example
    OTP.objects.create(email=email, code=otp, expires_at=datetime.utcnow() + timedelta(minutes=5))
    return otp
import random
from django.core.cache import cache

OTP_EXPIRY = 300 # 5 minutes

def generate_otp():
    return str(random.randint(10000,99999))

def save_otp(email,otp):
    cache.set(f"otp_{email}", otp, timeout=OTP_EXPIRY)

def get_otp(email):
    return cache.get(f"otp_{email}")

def delete_otp(email):
    cache.delete(f"otp_{email}")


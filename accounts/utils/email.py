from django.core.mail import send_mail
from django.conf import settings

def send_otp_email(email, otp):
    subject = "Password Reset OTP"
    message = f"""
Your OTP is: {otp}

This OTP will expire in 5 minutes.
If you didn't request this, ignore this email.
"""
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [email],
        fail_silently=False,
    )

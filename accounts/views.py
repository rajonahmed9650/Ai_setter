from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.core.cache import cache
from django.contrib.auth import get_user_model
from .serializers import (
    LoginSerializer,
    ForgotPasswordSerializer,
    OTPVerifySerializer,
    ResetPasswordSerializer,
    ProfileSerializer,
)
from .utils.email import send_otp_email
from .utils.otp import(
    generate_otp,
    save_otp,
    get_otp,
    delete_otp,
)
from .models import Profile

User = get_user_model()

class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data)


class ForgotPassowordView(APIView):
    permission_classes = [AllowAny]

    def post(self,request):
        serializer = ForgotPasswordSerializer(data = request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]
        user = User.objects.filter(email=email).first()
        if not user:
            return Response({"error":"User not found"},status=404)
        
        otp = generate_otp()
        save_otp(email,otp)
        send_otp_email(email,otp)
        print("otp:",otp)

        return Response({"message":"OTP send to email"})
    

class OTPVerifyView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = OTPVerifySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]
        otp_input = serializer.validated_data["otp"]

        saved_otp = cache.get(f"otp_{email}")
        if not saved_otp:
            return Response({"error": "OTP expired"}, status=400)

        if saved_otp != otp_input:
            return Response({"error": "Invalid OTP"}, status=400)

        # ✅ OTP verified → EMAIL cache এ রাখো
        cache.set("otp_verified_email", email, timeout=300)  # 5 min

        # cleanup
        cache.delete(f"otp_{email}")

        return Response({
            "message": "OTP verified successfully"
        })

            

class ResetPasswordView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = ResetPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        new_password = serializer.validated_data["new_password"]

        email = cache.get("otp_verified_email")
        if not email:
            return Response(
                {"error": "OTP not verified or expired"},
                status=403
            )

        user = User.objects.filter(email=email).first()
        if not user:
            return Response({"error": "User not found"}, status=404)

        user.set_password(new_password)
        user.save()

        # one-time use
        cache.delete("otp_verified_email")

        return Response({
            "message": "Password reset successful"
        })


class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        profile, _ = Profile.objects.get_or_create(user=request.user)
        serializer = ProfileSerializer(profile,context={"request": request})
        return Response(serializer.data)
    def put(self, request):
        #  ensure profile exists
        profile, _ = Profile.objects.get_or_create(user=request.user)

        serializer = ProfileSerializer(profile,data=request.data,partial=True,context={"request": request})
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({
            "message": "Profile updated successfully",
            "data": serializer.data
        })


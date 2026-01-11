from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Profile

User = get_user_model()

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(write_only =True)
    password = serializers.CharField(write_only=True)

    access = serializers.CharField(read_only=True)
    refresh = serializers.CharField(read_only=True)

    def validate(self, data):
        email = data["email"]
        password = data["password"]

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError("Invalid credentials")

        if not user.check_password(password):
            raise serializers.ValidationError("Invalid credentials")

        if not user.is_superuser:
            raise serializers.ValidationError("Not allowed")

        refresh = RefreshToken.for_user(user)

        return {
            "access": str(refresh.access_token),
            "refresh": str(refresh),
        }

class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()

class OTPVerifySerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField()

class ResetPasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField(write_only = True , min_length = 6)
    confirm_password = serializers.CharField(write_only = True , min_length = 6)

    def validate(self, data):
        if data["new_password"]!=data["confirm_password"]:
            raise serializers.ValidationError(
                {"confirm_password":"Passwords do not match"}
            )
        return data


# accounts/serializers.py
from rest_framework import serializers
from .models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(source="user.first_name",required=False)
    last_name = serializers.CharField(source="user.last_name",required=False)
    email = serializers.EmailField(source="user.email",read_only=True)

    class Meta:
        model = Profile
        fields = ["first_name","last_name","email","image","business_name","website",]

    def update(self, instance, validated_data):
        # 🔹 nested user data
        user_data = validated_data.pop("user", None)

        # 🔹 update User table
        if user_data:
            if "first_name" in user_data:
                instance.user.first_name = user_data["first_name"]
            if "last_name" in user_data:
                instance.user.last_name = user_data["last_name"]
            instance.user.save()

   
        instance = super().update(instance, validated_data)

        return instance
   
       
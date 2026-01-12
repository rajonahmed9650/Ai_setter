from django.urls import path
from .views import(
    LoginView,
    ForgotPassowordView,
    OTPVerifyView,
    ResetPasswordView,
    ProfileView,
    CreateUserView
)


urlpatterns = [
    path("auth/login", LoginView.as_view(), name="login"),
    path("auth/forgot-password", ForgotPassowordView.as_view(), name="forgot-password"),
    path("auth/verify-otp", OTPVerifyView.as_view(), name="verify-otp"),
    path("auth/reset-password", ResetPasswordView.as_view(), name="reset-password"),
    path("auth/profile",ProfileView.as_view(), name="reset-password"),
    path("create-user",CreateUserView.as_view(),name="create-user")
]

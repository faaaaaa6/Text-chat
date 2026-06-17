from django.urls import path
from .views import RegisterView , ResendOTPView , VerifyOTPView

urlpatterns = [
    path('register/',RegisterView.as_view(), name='register'),
    path('resend-otp/', ResendOTPView.as_view(), name='resend-otp'),
    path('verify-otp/', VerifyOTPView.as_view(), name='verify-otp')
]

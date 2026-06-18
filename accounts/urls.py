from django.urls import path
from .views import RegisterView , ResendOTPView , VerifyOTPView,LoginView,LogoutView,ProfileView, UpdateProfileView,ChangePasswordView

urlpatterns = [

    path('register/',RegisterView.as_view(), name='register'),

    path('resend-otp/', ResendOTPView.as_view(), name='resend-otp'),
    path('verify-otp/', VerifyOTPView.as_view(), name='verify-otp'),
    
    path('login/', LoginView.as_view(), name='login'),
    path('logout/',LogoutView.as_view(),name='logout'),

    path('profile/',ProfileView.as_view(), name='profile'),
    path('profile/update/',UpdateProfileView.as_view(),name='update-profile'),

    path('change-password/',ChangePasswordView.as_view(), name='change-password'),

]

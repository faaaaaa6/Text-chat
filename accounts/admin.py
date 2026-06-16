from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser,OTPVerification

@admin.register(CustomUser)#for registring customuser in admin panel 
class CustomUserAdmin(UserAdmin):
    list_display = ('username' ,'email' , 'phone_number' , 'is_online' , 'last_seen')
    fieldset = UserAdmin.fieldsets + (
        
        ('Extra_Info',{'fields':('phone_number','profile_picture','bio','is_online','last_seen')}),
    )

@admin.register(OTPVerification)
class OTPVerificationAdmin(admin.ModelAdmin):
    list_display = ('user' , 'otp' , 'created_at', 'is_verified')
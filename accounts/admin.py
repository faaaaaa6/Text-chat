from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

@admin.register(CustomUser)#for registring customuser in admin panel 
class CustomUserAdmin(UserAdmin):
    list_display = ('username' ,'email' , 'phone_number' , 'is_online' , 'last_seen')
    fieldset = UserAdmin.fieldsets + (
        
        ('Extra_Info',{'fields':('phone_number','profile_picture','bio','is_online','last_seen')}),
    )



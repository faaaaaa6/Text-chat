from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import CustomUser


class RegisterSerializer(serializers.Serializer):
   first_name = serializers.CharField(required=True)
   last_name = serializers.CharField(required =True)
   username = serializers.CharField(required = True)
   email = serializers.EmailField(required = True)
   phone_number =serializers.CharField(required = True)

   #for checking the password matching and password strength: 
   password = serializers.CharField(
       write_only=True,
       required=True,
       validators=[validate_password]   
   )

   password2 =serializers.CharField(
       write_only=True,
       required=True
   )
   #adding validation function for each method:

   #username format rules!
   def validate_username(self, value):
       if CustomUser.objects.filter(username=value).exists():
           raise serializers.ValidationError("Username already exists")
      
       if len(value) < 3:
           raise serializers.ValidationError("Username must be at least 3 characters")
       
       if ' ' in value:
           raise serializers.ValidationError("Username cannot contain spaces")
      
       return value
   
   #email format rules!

   def validate_email(self,value):
       if CustomUser.objects.filter(email=value).exists():
           raise serializers.ValidationError("Email already registered")
       
       return value.lower()
   
   #phone_number foramt rules!

   def validate_phone_number(self, value):
       if CustomUser.objects.filter(phone_number=value).exists():
           raise serializers.ValidationError("phone number already registered")
       
       if not value.isdigit():
           raise serializers.ValidationError("phone number must contain only digits")
         
       if  len(value) <10 or len(value) > 15:
           raise serializers.ValidationError("Phone number must be between 10 and 15 digits")
       return value
   
   #password double check rules!

   def validate(self, data):
       if data['password'] !=data['password2']:
           raise serializers.ValidationError({"password": "Password don't match"})
       return data
   
   #first and second name rules
  
   def validate_first_name(self,value):
       if not value.isalpha():
           raise serializers.ValidationError("first name must contain only letters")
       return value.capitalize()
   
   def validate_last_name(self,value):
       if not value.isalpha():
           raise serializers.ValidationError("last name must contain only letters")
       
       return value.capitalize()
   
   def validate_profile_picture(self,value):
       if value.size > 2 * 1024 * 1024:
           raise serializers.ValidationError("profile picture must be under 2MB")
       return value
   
   #for removing the password2 field from the database saving 
   def create(self, validated_data):
       validated_data.pop('password2')
       #create_user create a hashed password for user security
       user =CustomUser.objects.create_user(
           username=validated_data['username'],
           email=validated_data['email'],
           phone_number=validated_data['phone_number'],
           first_name=validated_data['first_name'],
           last_name=validated_data['last_name'],
           password=validated_data['password']
       )
       return user
           

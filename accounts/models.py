from django.db import models
from django.contrib.auth.models import AbstractUser
import random
from django.utils import timezone

class CustomUser(AbstractUser):#django automatically build username,emails,password,first name and last name.
    phone_number = models.CharField(max_length=15, unique = True, null = True, blank = True)
    profile_picture = models.ImageField(upload_to ='profile_pics/', null = True , blank = True)
    bio = models.TextField(null=True, blank =True)
    is_online = models.BooleanField(default = False)
    last_seen  = models.DateTimeField(null = True ,blank = True)

    def __str__(self):
        return self.username

#str is used to show the username instead of user id as output

#creating a model to store the otp in database for validation

class OTPVerification(models.Model):
    user = models.OneToOneField(CustomUser , on_delete=models.CASCADE)
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    is_verified = models.BooleanField(default=False)

    def generate_otp(self):
        self.otp = str(random.randint(100000,999999))
        self.created_at = timezone.now()
        self.save()
        return self.otp
    
    def is_expired(self):
        expiry_time = self.created_at + timezone.timedelta(minutes=10)
        return timezone.now() > expiry_time
    
    def __str__(self):
        return f"{self.user.username} - {self.otp}"

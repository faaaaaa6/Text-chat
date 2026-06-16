from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):#django automatically build username,emails,password,first name and last name.
    phone_number = models.CharField(max_length=15, unique = True, null = True, blank = True)
    profile_picture = models.ImageField(upload_to ='profile_pics/', null = True , blank = True)
    bio = models.TextField(null=True, blank =True)
    is_online = models.BooleanField(default = False)
    last_seen  = models.DateTimeField(null = True ,blank = True)

    def __str__(self):
        return self.username

#str is used to show the username instead of user id as output
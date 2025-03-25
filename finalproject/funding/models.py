from datetime import timedelta
from django.db import models
import uuid
from django.utils.timezone import now

# Create your models here.
class Profile(models.Model):
    name = models.CharField(max_length=100)
    profile_picture = models.ImageField(upload_to='profile_pics/', default='profile_pics/default.png')

    def __str__(self):
        return self.name
    
class UserProfile(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)  
    phone = models.CharField(max_length=15, unique=True)
    picture = models.ImageField(upload_to='profile_pics/', default='profile_pics/default.jpg')
    is_active = models.BooleanField(default=False)  
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"

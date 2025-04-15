from decimal import Decimal
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from django.contrib.auth.models import User

class UserProfileManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

class UserProfile(AbstractBaseUser):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=15, unique=True)
    picture = models.ImageField(upload_to='profile_pics/')
    is_active = models.BooleanField(default=False)
    facebook_profile = models.URLField(max_length=200, blank=True , null=True)
    birth_date = models.DateField(blank=True, null=True)
    country = models.CharField(max_length=50, blank=True, null=True)
    
    USERNAME_FIELD = 'email'  # Ensure this is set correctly
    REQUIRED_FIELDS = ['first_name', 'last_name', 'phone']

    objects = UserProfileManager()

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    
    def __str__(self):
        return self.name

class Project(models.Model):
    title = models.CharField(max_length=255)
    details = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='projects')
    total_target = models.DecimalField(max_digits=10, decimal_places=2)
    tags = models.CharField(max_length=255, help_text="Comma-separated tags")
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    current_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    user = models.ForeignKey("UserProfile", on_delete=models.CASCADE, null=True, blank=True)
    reported = models.BooleanField(default=False)
    cancelled = models.BooleanField(default=False)

    def __str__(self):
        return self.title
    
    def can_be_cancelled(self):
        return self.current_amount < (Decimal('0.25') * self.total_target)
    
    def average_rating(self):
        ratings = self.ratings.all()  
        if ratings.exists():
            return round(sum(rating.value for rating in ratings) / ratings.count(), 1)
        return 0
    
class CampaignImage(models.Model):
    campaign = models.ForeignKey(Project, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='campaigns/')

    def __str__(self):
        return f"Image for {self.campaign.title}"
    

class Donation(models.Model):
    user = models.ForeignKey("UserProfile", on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)


class Comment(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey("UserProfile", on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    reported = models.BooleanField(default=False)


class Rating(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="ratings")
    user = models.ForeignKey("UserProfile", on_delete=models.CASCADE)
    value = models.IntegerField() 
    created_at = models.DateTimeField(auto_now_add=True)

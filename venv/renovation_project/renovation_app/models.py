import os
from django.db import models
from django.contrib.auth.models import AbstractUser

def profile_image_upload_path(instance, filename):
    """Rename profile image as {usertype}_{username}_profile.jpg/png"""
    user_type = instance.usertype.lower()
    username = instance.username.lower()
    ext = filename.split('.')[-1]  # Get file extension (jpg/png)
    return os.path.join('profile_pics/', f"{user_type}_{username}_profile.{ext}")

def portfolio_upload_path(instance, filename):
    """Rename the uploaded file as {usertype}_{username}_portfolio.pdf"""
    user_type = instance.usertype.lower()  # Ensure lowercase for consistency
    username = instance.username.lower()
    new_filename = f"{user_type}_{username}_portfolio.pdf"
    return os.path.join('portfolios/', new_filename)

class Register(AbstractUser):
    usertype = models.CharField(max_length = 50, default = "admin")
    contact = models.IntegerField( null = True)
    image = models.ImageField(upload_to=profile_image_upload_path, null=True)
    experience = models.IntegerField(null = True)
    license_no = models.CharField(max_length = 21, null = True)
    location = models.URLField(max_length=2000, blank= True, null=True)
    specialization = models.CharField(max_length = 50, blank= True, null = True)
    is_approved = models.BooleanField(blank= True, default=True)
    portfolio = models.FileField(upload_to=portfolio_upload_path, blank= True, null = True)

class Reset(models.Model):
    otp = models.CharField(max_length=6, null=True)
    user = models.ForeignKey(Register, on_delete=models.CASCADE,null=True)
    otp_created_at = models.DateTimeField(auto_now_add = True)
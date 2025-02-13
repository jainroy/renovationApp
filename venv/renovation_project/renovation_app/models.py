from django.db import models
from django.contrib.auth.models import AbstractUser

class Register(AbstractUser):
    usertype = models.CharField(max_length = 50, default = "admin")
    contact = models.IntegerField( null = True)
    image = models.ImageField(upload_to = 'uploads/', null = True)
    experience = models.IntegerField(null = True)
    license_no = models.CharField(max_length = 20, null = True)

class Reset(models.Model):
    otp = models.CharField(max_length=6, null=True)
    user = models.ForeignKey(Register, on_delete=models.CASCADE,null=True)
    otp_created_at = models.DateTimeField(auto_now_add = True)
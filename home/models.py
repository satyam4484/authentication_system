from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class userprofile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    reset_pass_token = models.CharField(max_length=100)
    email_verify = models.CharField(max_length=100)
    is_verified = models.BooleanField(default=False)

    

from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    pass

class UserProfile(models.Model):
    uniq_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length = 255)
    last_name = models.CharField(max_length = 255)
    dob = models.DateField(blank=True, null=True)
    aadhar = models.ForeignKey(User,to_field='username',null=True, on_delete=models.SET_NULL)
    gender = models.ForeignKey('election.ElectionDropdown',null=True, on_delete=models.SET_NULL)

class UserAddress(models.Model):
    uniq_id = models.ForeignKey(UserProfile,on_delete=models.CASCADE)
    full_address = models.CharField(max_length=500)
    state = models.CharField(max_length=255)
    constituency = models.CharField(max_length=255)


class OfficialsDetails(models.Model):
    id = models.AutoField(primary_key=True)
    official = models.ForeignKey(User,to_field='username',null=True, on_delete=models.SET_NULL)
    user = models.ForeignKey(UserProfile,on_delete=models.CASCADE)
    desg = models.ForeignKey('election.ElectionDropdown',null=True, on_delete=models.SET_NULL)

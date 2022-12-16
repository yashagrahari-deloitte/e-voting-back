from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    user_type = models.CharField(max_length = 16)

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

class LeftPanel(models.Model):
    sno = models.AutoField(db_column='Sno',primary_key=True)
    pid = models.IntegerField(db_column='Pid', blank=True, null=True)
    name = models.CharField(max_length=512,default=None)
    route = models.CharField(max_length=512,default=None)
    icon = models.CharField(max_length=64,null=True,default=None)
    priority = models.IntegerField(default=None)


class Roles(models.Model):
    id = models.AutoField(primary_key=True)
    official = models.ForeignKey('home.OfficialsDetails',null=True, on_delete=models.CASCADE)
    item_id = models.ForeignKey('home.LeftPanel',null=True,on_delete=models.CASCADE)
from django.db import models
from django.db.models import JSONField


class ElectionDropdown(models.Model):
    sno = models.AutoField(db_column='Sno',primary_key=True)
    pid = models.IntegerField(db_column='Pid', blank=True, null=True)
    field = models.CharField(db_column='Field', max_length=255, blank=True, null=True)
    value = models.CharField(db_column='Value', max_length=255, blank=True, null=True)
    status = models.CharField(max_length=16, blank=True, null=True)

    class Meta:
        managed = True

class Electiontiming(models.Model):
    uid = models.IntegerField(db_column='Uid',primary_key=True) 
    session = models.CharField(max_length=16, blank=True, null=True)
    session_name = models.CharField(max_length=8)

    class Meta:
        managed = True

class ElectionInfo(models.Model):
    title = models.CharField(max_length=255)
    description_language = JSONField(default=dict)
    election_type = models.ForeignKey('ElectionDropdown', on_delete=models.PROTECT)
    phases = models.IntegerField()
    session = models.ForeignKey('Electiontiming', on_delete=models.PROTECT)

    class Meta:
        managed = True

class ElectionLockingUnlocking(models.Model):
    lock_type = models.CharField(max_length=8)
    unlock_from = models.DateTimeField(default=None, null=True)
    unlock_to = models.DateTimeField(default=None, null=True)
    status = models.CharField(db_column='status', default='INSERT', max_length=16)
    # unlocked_by = models.ForeignKey()
    session = models.ForeignKey('Electiontiming', on_delete=models.PROTECT)
    created_at = models.DateTimeField(db_column='created_at',auto_now=True)

    class Meta:
        managed = True
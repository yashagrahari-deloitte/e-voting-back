from django.db import models
from home.models import OfficialsDetails

class ElectionPhaseWiseState_2022(models.Model):
    uid = models.AutoField(db_column='Uid',primary_key=True)
    election_id = models.ForeignKey('election.ElectionInfo', on_delete=models.CASCADE)
    phase = models.CharField(max_length=16)
    state = models.CharField(max_length=255)
    created_at = models.DateTimeField(db_column='created_at',auto_now=True)
    session = models.ForeignKey('Electiontiming', default=None, null=True, on_delete=models.PROTECT)

    class Meta:
        managed = True

class ElectionStateWiseConsituency_2022(models.Model):
    uid = models.AutoField(db_column='Uid',primary_key=True)
    phase_stateid = models.ForeignKey('election.ElectionPhaseWiseState_2022', on_delete=models.CASCADE)
    constituency = models.CharField(max_length=255)
    created_at = models.DateTimeField(db_column='created_at',auto_now=True)
    session = models.ForeignKey('Electiontiming',null=True,default=None,on_delete=models.PROTECT)

    class Meta:
        managed = True

    
class ElectionRolesAssigned_2022(models.Model):
    uid = models.AutoField(db_column='Uid',primary_key=True)
    election_id = models.ForeignKey('election.ElectionInfo', on_delete=models.CASCADE)
    phase_stateid = models.ForeignKey('election.ElectionPhaseWiseState_2022', on_delete=models.CASCADE)
    constituency_id = models.ForeignKey('election.ElectionStateWiseConsituency_2022',on_delete=models.CASCADE)
    assigned_to = models.ForeignKey(OfficialsDetails,default=None, null=True, on_delete=models.CASCADE)
    roles = models.ForeignKey('ElectionDropdown',  default=None, on_delete=models.PROTECT)
    created_at = models.DateTimeField(db_column='created_at',auto_now=True)
    session = models.ForeignKey('Electiontiming',null=True, default=None, on_delete=models.PROTECT)

    class Meta:
        managed = True


class ElectionLockingUnlocking_2022(models.Model):
    id = models.AutoField(db_column='Uid',primary_key=True)
    phase = models.CharField(max_length=8)
    starttime=  models.DateTimeField(default=None, null=True) 
    endtime =  models.DateTimeField(default=None, null=True)
    election_id = models.ForeignKey('election.ElectionInfo', on_delete=models.CASCADE)
    lockType = models.ForeignKey('election.ElectionDropdown', on_delete=models.CASCADE)
    unlocked_by = models.ForeignKey(OfficialsDetails,default=None, null=True, on_delete=models.CASCADE)
    created_at = models.DateTimeField(db_column='created_at',auto_now=True)
    session = models.ForeignKey('Electiontiming',null=True, default=None, on_delete=models.PROTECT)

    class Meta:
        managed = True


class ElectionCandidates_2022(models.Model):
    id = models.AutoField(db_column='Uid',primary_key=True)
    candidate_id = models.ForeignKey('home.UserProfile',null=True, default=None, on_delete=models.CASCADE)
    constituency = models.ForeignKey('election.ElectionStateWiseConsituency_2022',on_delete=models.CASCADE)
    party = models.ForeignKey('election.ElectionDropdown', related_name='ElectionParty_2022' ,default=None, on_delete=models.PROTECT)
    religion = models.ForeignKey('election.ElectionDropdown', related_name='ElectionReligion_2022', default=None, on_delete=models.PROTECT)
    session = models.ForeignKey('Electiontiming',null=True, default=None, on_delete=models.PROTECT)
    is_Indian = models.BooleanField(default=True)
    qualification = models.JSONField(default=dict)


class EligibleVoters_2022(models.Model):
    id = models.AutoField(db_column='Uid',primary_key=True)
    uniq_id = models.ForeignKey('home.UserProfile',null=True, default=None, on_delete=models.CASCADE)
    constituency = models.CharField(max_length=512)
    age = models.IntegerField()
    is_voted = models.BooleanField(default=True)
    status = models.CharField(max_length=16, blank=True, null=True,default='INSERT')
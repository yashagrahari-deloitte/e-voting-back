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
    phase = models.CharField(max_length=8)
    startDate =  models.DateTimeField(default=None, null=True) 
    endDate =  models.DateTimeField(default=None, null=True)
    electionName = models.ForeignKey('election.ElectionInfo', on_delete=models.CASCADE)
    lockType = models.ForeignKey('election.ElectionDropdown', on_delete=models.CASCADE)
    unlocked_by = models.ForeignKey(OfficialsDetails,default=None, null=True, on_delete=models.CASCADE)
    created_at = models.DateTimeField(db_column='created_at',auto_now=True)
    session = models.ForeignKey('Electiontiming',null=True, default=None, on_delete=models.PROTECT)

    class Meta:
        managed = True


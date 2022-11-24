from django.db import models
from home.models import OfficialsDetails

class ElectionPhaseWiseState_2022(models.Model):
    uid = models.AutoField(db_column='Uid',primary_key=True)
    election_id = models.ForeignKey('election.ElectionInfo', on_delete=models.CASCADE)
    phase = models.CharField(max_length=16)
    state = models.CharField(max_length=255)

    class Meta:
        managed = True

class ElectionStateWiseConsituency_2022(models.Model):
    uid = models.AutoField(db_column='Uid',primary_key=True)
    phase_stateid = models.ForeignKey('election.ElectionPhaseWiseState_2022', on_delete=models.CASCADE)
    constituency = models.CharField(max_length=255)

    class Meta:
        managed = True

    
class ElectionRolesAssigned_2022(models.Model):
    uid = models.AutoField(db_column='Uid',primary_key=True)
    election_id = models.ForeignKey('election.ElectionInfo', on_delete=models.CASCADE)
    phase_stateid = models.ForeignKey('election.ElectionPhaseWiseState_2022', on_delete=models.CASCADE)
    constituency_id = models.ForeignKey('election.ElectionStateWiseConsituency_2022',on_delete=models.CASCADE)
    assigned_to = models.ForeignKey(OfficialsDetails,default=None, null=True, on_delete=models.CASCADE)
    roles = models.ForeignKey('ElectionDropdown', on_delete=models.PROTECT)
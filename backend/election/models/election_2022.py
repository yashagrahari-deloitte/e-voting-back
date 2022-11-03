from django.db import models

class ElectionPhaseWiseState_2022(models.Model):
    uid = models.IntegerField(db_column='Uid',primary_key=True)
    election_id = models.ForeignKey('election.ElectionInfo', on_delete=models.CASCADE)
    phase = models.CharField(max_length=4)
    state = models.CharField(max_length=255)

    class Meta:
        managed = True

class ElectionStateWiseConsituency_2022(models.Model):
    uid = models.IntegerField(db_column='Uid',primary_key=True)
    phase_stateid = models.ForeignKey('election.ElectionPhaseWiseState_2022', on_delete=models.CASCADE)
    constituency = models.CharField(max_length=255)

    class Meta:
        managed = True

    


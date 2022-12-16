# Generated by Django 3.2 on 2022-12-16 09:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('home', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='ElectionDropdown',
            fields=[
                ('sno', models.AutoField(db_column='Sno', primary_key=True, serialize=False)),
                ('pid', models.IntegerField(blank=True, db_column='Pid', null=True)),
                ('field', models.CharField(blank=True, db_column='Field', max_length=255, null=True)),
                ('value', models.CharField(blank=True, db_column='Value', max_length=255, null=True)),
                ('status', models.CharField(blank=True, default='INSERT', max_length=16, null=True)),
            ],
            options={
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='ElectionInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('description_language', models.JSONField(default=dict)),
                ('phases', models.IntegerField()),
                ('status', models.CharField(blank=True, default='INSERT', max_length=16, null=True)),
                ('current_status', models.CharField(blank=True, max_length=32, null=True)),
                ('added_by', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='home.officialsdetails')),
                ('election_type', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='election.electiondropdown')),
            ],
            options={
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='ElectionPhaseWiseState_2022',
            fields=[
                ('uid', models.AutoField(db_column='Uid', primary_key=True, serialize=False)),
                ('phase', models.CharField(max_length=16)),
                ('state', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now=True, db_column='created_at')),
                ('election_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='election.electioninfo')),
            ],
            options={
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Electiontiming',
            fields=[
                ('uid', models.IntegerField(db_column='Uid', primary_key=True, serialize=False)),
                ('session', models.CharField(blank=True, max_length=16, null=True)),
                ('session_name', models.CharField(max_length=8)),
            ],
            options={
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='EligibleVoters_2022',
            fields=[
                ('id', models.AutoField(db_column='Uid', primary_key=True, serialize=False)),
                ('constituency', models.CharField(max_length=512)),
                ('age', models.IntegerField()),
                ('is_voted', models.BooleanField(default=True)),
                ('status', models.CharField(blank=True, default='INSERT', max_length=16, null=True)),
                ('uniq_id', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='home.userprofile')),
            ],
        ),
        migrations.CreateModel(
            name='ElectionStateWiseConsituency_2022',
            fields=[
                ('uid', models.AutoField(db_column='Uid', primary_key=True, serialize=False)),
                ('constituency', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now=True, db_column='created_at')),
                ('phase_stateid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='election.electionphasewisestate_2022')),
                ('session', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.PROTECT, to='election.electiontiming')),
            ],
            options={
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='ElectionRolesAssigned_2022',
            fields=[
                ('uid', models.AutoField(db_column='Uid', primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now=True, db_column='created_at')),
                ('status', models.CharField(blank=True, default='INSERT', max_length=16, null=True)),
                ('assigned_to', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='home.officialsdetails')),
                ('constituency_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='election.electionstatewiseconsituency_2022')),
                ('election_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='election.electioninfo')),
                ('phase_stateid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='election.electionphasewisestate_2022')),
                ('roles', models.ForeignKey(default=None, on_delete=django.db.models.deletion.PROTECT, to='election.electiondropdown')),
                ('session', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.PROTECT, to='election.electiontiming')),
            ],
            options={
                'managed': True,
            },
        ),
        migrations.AddField(
            model_name='electionphasewisestate_2022',
            name='session',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.PROTECT, to='election.electiontiming'),
        ),
        migrations.CreateModel(
            name='ElectionLockingUnlocking_2022',
            fields=[
                ('id', models.AutoField(db_column='Uid', primary_key=True, serialize=False)),
                ('phase', models.CharField(max_length=8)),
                ('starttime', models.DateTimeField(default=None, null=True)),
                ('endtime', models.DateTimeField(default=None, null=True)),
                ('created_at', models.DateTimeField(auto_now=True, db_column='created_at')),
                ('election_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='election.electioninfo')),
                ('lockType', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='election.electiondropdown')),
                ('session', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.PROTECT, to='election.electiontiming')),
                ('unlocked_by', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='home.officialsdetails')),
            ],
            options={
                'managed': True,
            },
        ),
        migrations.AddField(
            model_name='electioninfo',
            name='session',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.PROTECT, to='election.electiontiming'),
        ),
        migrations.CreateModel(
            name='ElectionCandidates_2022',
            fields=[
                ('id', models.AutoField(db_column='Uid', primary_key=True, serialize=False)),
                ('is_Indian', models.BooleanField(default=True)),
                ('qualification', models.JSONField(default=dict)),
                ('candidate_id', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='home.userprofile')),
                ('constituency', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='election.electionstatewiseconsituency_2022')),
                ('party', models.ForeignKey(default=None, on_delete=django.db.models.deletion.PROTECT, related_name='ElectionParty_2022', to='election.electiondropdown')),
                ('religion', models.ForeignKey(default=None, on_delete=django.db.models.deletion.PROTECT, related_name='ElectionReligion_2022', to='election.electiondropdown')),
                ('session', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.PROTECT, to='election.electiontiming')),
            ],
        ),
    ]

# Generated by Django 3.2 on 2022-11-04 07:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_officialsdetails_useraddress_userprofile'),
    ]

    operations = [
        migrations.RenameField(
            model_name='officialsdetails',
            old_name='official_id',
            new_name='official',
        ),
        migrations.RenameField(
            model_name='officialsdetails',
            old_name='user_id',
            new_name='user',
        ),
        migrations.RenameField(
            model_name='userprofile',
            old_name='aadhar_id',
            new_name='aadhar',
        ),
    ]
# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.contrib.auth.models import AbstractUser

'''
To synchronize the database, refer to this link:
https://blog.csdn.net/vainfanfan/article/details/80556429
'''


class Condition(models.Model):
    condition_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=70, blank=True, null=True)
    value = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Condition'
        unique_together = (('name', 'value'),)


class Reminder(models.Model):
    reminder_id = models.AutoField(primary_key=True)
    start_time = models.DateField(blank=True, null=True)
    end_time = models.DateField(blank=True, null=True)
    frequency = models.TimeField(blank=True, null=True)
    user = models.ForeignKey('Userinfo', models.DO_NOTHING, blank=True, null=True)
    treatment = models.ForeignKey('Treatment', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Reminder'


class Role(models.Model):
    role_id = models.AutoField(primary_key=True)
    role_name = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Role'


class Symptom(models.Model):
    symptom_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    value = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Symptom'


class Tag(models.Model):
    tag_id = models.AutoField(primary_key=True)
    name = models.CharField(unique=True, max_length=120, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Tag'


class Trackable(models.Model):
    trackable_id = models.IntegerField(primary_key=True)
    user = models.ForeignKey('Userinfo', models.DO_NOTHING, blank=True, null=True)
    public = models.IntegerField(blank=True, null=True)
    checkin_date = models.DateField(blank=True, null=True)
    tag = models.ForeignKey(Tag, models.DO_NOTHING, blank=True, null=True)
    condition = models.ForeignKey(Condition, models.DO_NOTHING, blank=True, null=True)
    weather = models.ForeignKey('Weather', models.DO_NOTHING, blank=True, null=True)
    treatment = models.ForeignKey('Treatment', models.DO_NOTHING, blank=True, null=True)
    symptom = models.ForeignKey(Symptom, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Trackable'


class Treatment(models.Model):
    treatment_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=40, blank=True, null=True)
    value = models.CharField(max_length=40, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Treatment'
        unique_together = (('name', 'value'),)


class Userinfo(models.Model):
    user_id = models.CharField(primary_key=True, max_length=100)
    username = models.CharField(max_length=70, blank=True, null=True)
    password = models.CharField(max_length=30, blank=True, null=True)
    age = models.IntegerField(blank=True, null=True)
    gender = models.CharField(max_length=30, blank=True, null=True)
    country = models.CharField(max_length=30, blank=True, null=True)
    email = models.CharField(max_length=50, blank=True, null=True)
    phone = models.CharField(max_length=30, blank=True, null=True)
    role = models.ForeignKey(Role, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'UserInfo'


class Weather(models.Model):
    weather_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=40, blank=True, null=True)
    value = models.CharField(max_length=30, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Weather'
        unique_together = (('name', 'value'),)

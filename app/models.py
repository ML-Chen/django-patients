# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Glasses(models.Model):
    patient = models.ForeignKey('Patient', models.CASCADE, db_column='patient', blank=True, null=True)
    prescription = models.ForeignKey('GlassesPrescription', models.SET_NULL, db_column='prescription', blank=True, null=True)
    date = models.DateTimeField(blank=True, null=True)
    brand = models.CharField(max_length=255, blank=True, null=True)
    model = models.CharField(max_length=255, blank=True, null=True)
    color = models.CharField(max_length=255, blank=True, null=True)
    frame = models.CharField(max_length=100, blank=True, null=True)
    lens = models.CharField(max_length=255, blank=True, null=True)
    contact_lens = models.CharField(max_length=255, blank=True, null=True)
    additional_comments = models.TextField(blank=True, null=True)
    price = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'glasses'


class GlassesPrescription(models.Model):
    patient = models.IntegerField(blank=True, null=True)
    exam_date = models.DateTimeField(blank=True, null=True)
    od = models.CharField(max_length=255, blank=True, null=True)
    os = models.CharField(max_length=255, blank=True, null=True)
    va_right = models.CharField(max_length=255, blank=True, null=True)
    va_left = models.CharField(max_length=255, blank=True, null=True)
    pd = models.FloatField(blank=True, null=True)
    conj = models.CharField(max_length=255, blank=True, null=True)
    sclera = models.CharField(max_length=255, blank=True, null=True)
    tears = models.CharField(max_length=255, blank=True, null=True)
    cornea = models.CharField(max_length=255, blank=True, null=True)
    iris = models.CharField(max_length=255, blank=True, null=True)
    antc = models.CharField(max_length=255, blank=True, null=True)
    cc = models.CharField(max_length=255, blank=True, null=True)
    lll = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'glasses_prescription'


class Insurance(models.Model):
    patient = models.ForeignKey('Patient', models.CASCADE, db_column='patient', blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    first_name = models.CharField(max_length=255, blank=True, null=True)
    dob = models.DateTimeField(blank=True, null=True)
    insurance_id = models.CharField(max_length=255, blank=True, null=True)
    insurance_id_2 = models.CharField(max_length=255, blank=True, null=True)
    can_call = models.BooleanField(blank=True, null=True)
    called = models.BooleanField(blank=True, null=True)

    class Meta:
        db_table = 'insurance'


class Patient(models.Model):
    last_name = models.CharField(max_length=255, blank=True, null=True)
    first_name = models.CharField(max_length=255, blank=True, null=True)
    dob = models.DateTimeField(blank=True, null=True)
    phone = models.CharField(max_length=255, blank=True, null=True)
    phone_2 = models.CharField(max_length=255, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    gender = models.CharField(max_length=1, blank=True, null=True)
    downstairs = models.BooleanField(blank=True, null=True)

    class Meta:
        db_table = 'patient'

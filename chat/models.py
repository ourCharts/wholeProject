# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Myorder(models.Model):
    order_id = models.CharField(primary_key=True, max_length=50)
    start_time = models.IntegerField()
    end_time = models.IntegerField()
    start_longitude = models.FloatField()
    start_latitude = models.FloatField()
    end_longitude = models.FloatField()
    end_latitude = models.FloatField()

    class Meta:
        managed = False
        db_table = 'myorder'


class Position(models.Model):
    driver_id = models.CharField(max_length=50)
    order_id = models.CharField(max_length=50)
    time_stamp = models.IntegerField(primary_key=True)
    longitude = models.FloatField()
    latitude = models.FloatField()

    class Meta:
        managed = False
        db_table = 'position'
        unique_together = (('time_stamp', 'order_id'),)

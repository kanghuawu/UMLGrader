# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models


class TenantData(models.Model):
    record_id = models.CharField(db_column='RECORD_ID', max_length=45)  # Field name made lowercase.
    tenant_id = models.CharField(db_column='TENANT_ID', max_length=10)  # Field name made lowercase.
    column_1 = models.CharField(db_column='COLUMN_1', max_length=80, blank=True, null=True)  # Field name made lowercase.
    column_2 = models.CharField(db_column='COLUMN_2', max_length=80, blank=True, null=True)  # Field name made lowercase.
    column_3 = models.CharField(db_column='COLUMN_3', max_length=80, blank=True, null=True)  # Field name made lowercase.
    column_4 = models.CharField(db_column='COLUMN_4', max_length=80, blank=True, null=True)  # Field name made lowercase.
    column_5 = models.CharField(db_column='COLUMN_5', max_length=80, blank=True, null=True)  # Field name made lowercase.

    def __str__(self):
        return str(self.record_id)+" "+str(self.tenant_id)+" "+str(self.column_1)+" "+str(self.column_2)

    class Meta:
        # managed = False
        db_table = 'TENANT_DATA'
        unique_together = (('tenant_id', 'record_id'),)
    def getFields(self, ln):
        re = [self.record_id, self.column_1, self.column_2, self.column_3, self.column_4, self.column_5]
        return re[:ln]


class TenantFields(models.Model):
    tenant = models.ForeignKey('TenantTable', models.DO_NOTHING, db_column='TENANT_ID')  # Field name made lowercase.
    field_name = models.CharField(db_column='FIELD_NAME', max_length=45)  # Field name made lowercase.
    field_type = models.CharField(db_column='FIELD_TYPE', max_length=80, blank=True, null=True)  # Field name made lowercase.
    field_column = models.IntegerField(db_column='FIELD_COLUMN')  # Field name made lowercase.

    def __str__(self):
        return str(self.tenant_id)+" "+str(self.field_name)+" "+str(self.field_column)

    class Meta:
        # managed = False
        db_table = 'TENANT_FIELDS'
        unique_together = (('tenant', 'field_name'),)


class TenantTable(models.Model):
    tenant_id = models.CharField(db_column='TENANT_ID', primary_key=True, max_length=10)  # Field name made lowercase.
    tenant_pass = models.CharField(db_column='TENANT_PASS', max_length=45)  # Field name made lowercase.

    def __str__(self):
        return str(self.tenant_id)+" "+str(self.tenant_pass)

    class Meta:
        # managed = False
        db_table = 'TENANT_TABLE'

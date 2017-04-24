# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-24 01:29
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TenantData',
            fields=[
                ('record_id', models.CharField(db_column='RECORD_ID', max_length=45)),
                ('tenant_id', models.CharField(db_column='TENANT_ID', max_length=10, primary_key=True, serialize=False)),
                ('column_1', models.CharField(blank=True, db_column='COLUMN_1', max_length=80, null=True)),
                ('column_2', models.CharField(blank=True, db_column='COLUMN_2', max_length=80, null=True)),
                ('column_3', models.CharField(blank=True, db_column='COLUMN_3', max_length=80, null=True)),
                ('column_4', models.CharField(blank=True, db_column='COLUMN_4', max_length=80, null=True)),
                ('column_5', models.CharField(blank=True, db_column='COLUMN_5', max_length=80, null=True)),
            ],
            options={
                'db_table': 'TENANT_DATA',
            },
        ),
        migrations.CreateModel(
            name='TenantTable',
            fields=[
                ('tenant_id', models.CharField(db_column='TENANT_ID', max_length=10, primary_key=True, serialize=False)),
                ('tenant_pass', models.CharField(db_column='TENANT_PASS', max_length=45)),
            ],
            options={
                'db_table': 'TENANT_TABLE',
            },
        ),
        migrations.CreateModel(
            name='TenantFields',
            fields=[
                ('tenant', models.ForeignKey(db_column='TENANT_ID', on_delete=django.db.models.deletion.DO_NOTHING, primary_key=True, serialize=False, to='tenant_grader.TenantTable')),
                ('field_name', models.CharField(db_column='FIELD_NAME', max_length=45)),
                ('field_type', models.CharField(blank=True, db_column='FIELD_TYPE', max_length=80, null=True)),
                ('field_column', models.IntegerField(db_column='FIELD_COLUMN')),
            ],
            options={
                'db_table': 'TENANT_FIELDS',
            },
        ),
        migrations.AlterUniqueTogether(
            name='tenantdata',
            unique_together=set([('tenant_id', 'record_id')]),
        ),
        migrations.AlterUniqueTogether(
            name='tenantfields',
            unique_together=set([('tenant', 'field_name')]),
        ),
    ]
# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2019-03-22 10:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0010_global_variable_setting_env_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='global_variable_setting',
            name='env_id',
            field=models.CharField(max_length=500),
        ),
        migrations.AlterField(
            model_name='global_variable_setting',
            name='project_id',
            field=models.CharField(max_length=500),
        ),
    ]
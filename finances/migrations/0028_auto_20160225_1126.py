# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-02-25 10:26
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finances', '0027_auto_20160225_1115'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lydia',
            name='time_operation',
            field=models.DateTimeField(default=datetime.datetime(2016, 2, 25, 11, 26, 18, 207674)),
        ),
    ]
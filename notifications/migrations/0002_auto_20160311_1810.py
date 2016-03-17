# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-03-11 17:10
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='type',
            field=models.CharField(choices=[('DEBUG', 'debug'), ('SUCCESS', 'success'), ('INFO', 'info'), ('WARNING', 'warning'), ('ERROR', 'error')], default='INFO', max_length=10),
        ),
    ]
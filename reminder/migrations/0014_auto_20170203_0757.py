# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-03 07:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reminder', '0013_auto_20170203_0756'),
    ]

    operations = [
        migrations.AlterField(
            model_name='note',
            name='user',
            field=models.CharField(max_length=10),
        ),
    ]

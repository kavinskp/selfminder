# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-03 07:59
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('reminder', '0014_auto_20170203_0757'),
    ]

    operations = [
        migrations.AlterField(
            model_name='note',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='reminder.Author'),
        ),
    ]

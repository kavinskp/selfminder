# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-19 16:35
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('reminder', '0023_customuser_is_verified'),
    ]

    operations = [
        migrations.AlterField(
            model_name='note',
            name='user',
            field=models.OneToOneField(default=1, on_delete=django.db.models.deletion.CASCADE, to='reminder.Owner'),
        ),
    ]
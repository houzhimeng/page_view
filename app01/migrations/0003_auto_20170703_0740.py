# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-03 07:40
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0002_application_hosttoapp'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='hosttoapp',
            name='aobj',
        ),
        migrations.RemoveField(
            model_name='hosttoapp',
            name='hobj',
        ),
        migrations.DeleteModel(
            name='HostToApp',
        ),
    ]

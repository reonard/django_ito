# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-02-24 14:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ticketmgr', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='incident',
            name='deliver_time',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='incident',
            name='take_time',
            field=models.DateTimeField(null=True),
        ),
    ]

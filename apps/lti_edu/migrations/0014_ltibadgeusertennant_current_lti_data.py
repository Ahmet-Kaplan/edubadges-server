# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-04-23 12:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lti_edu', '0013_auto_20190415_0634'),
    ]

    operations = [
        migrations.AddField(
            model_name='ltibadgeusertennant',
            name='current_lti_data',
            field=models.TextField(blank=True, null=True),
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2018-12-07 17:04


from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lti_edu', '0005_studentsenrolled_edu_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='studentsenrolled',
            name='denied',
            field=models.BooleanField(default=False),
        ),
    ]

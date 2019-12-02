# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-08-13 17:17


import badgeuser.managers
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('badgeuser', '0024_remove_badgeuser_user_type'),
    ]

    operations = [
        migrations.CreateModel(
            name='BadgeUserProxy',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
            },
            bases=('badgeuser.badgeuser',),
            managers=[
                ('objects', badgeuser.managers.BadgeUserManager()),
            ],
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-08-11 15:51


from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('badgeuser', '0022_badgeuser_faculty'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='badgeuser',
            options={'permissions': (('view_issuer_tab', 'User can view Issuer tab in front end'), ('has_faculty_scope', 'User has scope for faculty in Admin page'), ('has_institution_scope', 'User has scope for institution in Admin page')), 'verbose_name': 'badge user', 'verbose_name_plural': 'badge users'},
        ),
    ]

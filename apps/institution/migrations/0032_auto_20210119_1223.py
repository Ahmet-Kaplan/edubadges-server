# Generated by Django 2.2.13 on 2021-01-19 11:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('institution', '0031_auto_20201214_1630'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='faculty',
            unique_together=set(),
        ),
    ]

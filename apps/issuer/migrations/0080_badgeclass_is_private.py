# Generated by Django 2.2.14 on 2021-02-17 12:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('issuer', '0079_auto_20210131_1539'),
    ]

    operations = [
        migrations.AddField(
            model_name='badgeclass',
            name='is_private',
            field=models.BooleanField(default=False),
        ),
    ]
# Generated by Django 2.2.14 on 2021-02-18 12:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('issuer', '0081_auto_20210218_1336'),
    ]

    operations = [
        migrations.AlterField(
            model_name='issuer',
            name='name_english',
            field=models.CharField(max_length=512, null=True),
        ),
    ]

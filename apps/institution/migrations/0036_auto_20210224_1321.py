# Generated by Django 2.2.14 on 2021-02-24 12:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('institution', '0035_institution_default_language'),
    ]

    operations = [
        migrations.RenameField(
            model_name='faculty',
            old_name='name',
            new_name='name_english',
        ),
        migrations.AddField(
            model_name='faculty',
            name='name_dutch',
            field=models.CharField(max_length=512, null=True),
        ),
    ]

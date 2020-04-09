# Generated by Django 2.2.9 on 2020-03-05 13:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('staff', '0003_issuerstaff'),
    ]

    operations = [
        migrations.RenameField(
            model_name='badgeclassstaff',
            old_name='administrate_users',
            new_name='may_administrate_users',
        ),
        migrations.RenameField(
            model_name='badgeclassstaff',
            old_name='award',
            new_name='may_award',
        ),
        migrations.RenameField(
            model_name='badgeclassstaff',
            old_name='create',
            new_name='may_create',
        ),
        migrations.RenameField(
            model_name='badgeclassstaff',
            old_name='destroy',
            new_name='may_delete',
        ),
        migrations.RenameField(
            model_name='badgeclassstaff',
            old_name='read',
            new_name='may_read',
        ),
        migrations.RenameField(
            model_name='badgeclassstaff',
            old_name='sign',
            new_name='may_sign',
        ),
        migrations.RenameField(
            model_name='badgeclassstaff',
            old_name='update',
            new_name='may_update',
        ),
        migrations.RenameField(
            model_name='facultystaff',
            old_name='administrate_users',
            new_name='may_administrate_users',
        ),
        migrations.RenameField(
            model_name='facultystaff',
            old_name='award',
            new_name='may_award',
        ),
        migrations.RenameField(
            model_name='facultystaff',
            old_name='create',
            new_name='may_create',
        ),
        migrations.RenameField(
            model_name='facultystaff',
            old_name='destroy',
            new_name='may_delete',
        ),
        migrations.RenameField(
            model_name='facultystaff',
            old_name='read',
            new_name='may_read',
        ),
        migrations.RenameField(
            model_name='facultystaff',
            old_name='sign',
            new_name='may_sign',
        ),
        migrations.RenameField(
            model_name='facultystaff',
            old_name='update',
            new_name='may_update',
        ),
        migrations.RenameField(
            model_name='institutionstaff',
            old_name='administrate_users',
            new_name='may_administrate_users',
        ),
        migrations.RenameField(
            model_name='institutionstaff',
            old_name='award',
            new_name='may_award',
        ),
        migrations.RenameField(
            model_name='institutionstaff',
            old_name='create',
            new_name='may_create',
        ),
        migrations.RenameField(
            model_name='institutionstaff',
            old_name='destroy',
            new_name='may_delete',
        ),
        migrations.RenameField(
            model_name='institutionstaff',
            old_name='read',
            new_name='may_read',
        ),
        migrations.RenameField(
            model_name='institutionstaff',
            old_name='sign',
            new_name='may_sign',
        ),
        migrations.RenameField(
            model_name='institutionstaff',
            old_name='update',
            new_name='may_update',
        ),
        migrations.RenameField(
            model_name='issuerstaff',
            old_name='administrate_users',
            new_name='may_administrate_users',
        ),
        migrations.RenameField(
            model_name='issuerstaff',
            old_name='award',
            new_name='may_award',
        ),
        migrations.RenameField(
            model_name='issuerstaff',
            old_name='create',
            new_name='may_create',
        ),
        migrations.RenameField(
            model_name='issuerstaff',
            old_name='destroy',
            new_name='may_delete',
        ),
        migrations.RenameField(
            model_name='issuerstaff',
            old_name='read',
            new_name='may_read',
        ),
        migrations.RenameField(
            model_name='issuerstaff',
            old_name='sign',
            new_name='may_sign',
        ),
        migrations.RenameField(
            model_name='issuerstaff',
            old_name='update',
            new_name='may_update',
        ),
    ]
# Generated by Django 2.2.14 on 2021-03-29 15:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('directaward', '0006_auto_20210329_1545'),
        ('issuer', '0089_auto_20210329_1519'),
    ]

    operations = [
        migrations.AddField(
            model_name='badgeinstance',
            name='direct_award_bundle',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='directaward.DirectAwardBundle'),
        ),
    ]

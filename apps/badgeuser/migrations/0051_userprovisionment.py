# Generated by Django 2.2.9 on 2020-06-02 12:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('badgeuser', '0050_set_is_teacher'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProvisionment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('entity_id', models.CharField(default=None, max_length=254, unique=True)),
                ('email', models.EmailField(max_length=254)),
                ('object_id', models.PositiveIntegerField()),
                ('data', jsonfield.fields.JSONField(null=True)),
                ('for_teacher', models.BooleanField()),
                ('rejected', models.BooleanField(default=False)),
                ('type', models.CharField(choices=[('Invitation', 'Invitation')], max_length=254)),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.ContentType')),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]

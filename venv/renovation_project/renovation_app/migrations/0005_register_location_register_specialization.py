# Generated by Django 5.1.5 on 2025-02-07 16:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('renovation_app', '0004_register_experience_register_license_no'),
    ]

    operations = [
        migrations.AddField(
            model_name='register',
            name='location',
            field=models.URLField(max_length=2000, null=True),
        ),
        migrations.AddField(
            model_name='register',
            name='specialization',
            field=models.CharField(max_length=20, null=True),
        ),
    ]

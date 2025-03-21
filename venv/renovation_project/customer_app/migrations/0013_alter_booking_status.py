# Generated by Django 5.1.5 on 2025-02-28 06:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer_app', '0012_alter_booking_status_alter_roomdetails_room_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='status',
            field=models.CharField(choices=[('pending', 'Pending'), ('confirmed', 'Confirmed'), ('rejected', 'Rejected'), ('in_progress', 'In Progress'), ('completed', 'Completed'), ('cancelled', 'Cancelled')], default='pending', max_length=20),
        ),
    ]

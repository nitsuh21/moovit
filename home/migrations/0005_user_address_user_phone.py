# Generated by Django 5.0.6 on 2024-07-09 15:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0004_driver_level_driver_points'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='address',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='phone',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]

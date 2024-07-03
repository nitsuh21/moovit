# Generated by Django 5.0.6 on 2024-07-03 07:45

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item_name', models.CharField(blank=True, max_length=100, null=True)),
                ('item_type', models.CharField(default='Parcel', max_length=100)),
                ('orderID', models.CharField(max_length=100)),
                ('height', models.IntegerField(default=0)),
                ('width', models.IntegerField(default=0)),
                ('length', models.IntegerField(default=0)),
                ('weight', models.IntegerField(default=0)),
                ('quantity', models.IntegerField(default=1)),
                ('order_date', models.DateField(auto_now_add=True)),
                ('pickup_address', models.CharField(max_length=100)),
                ('delivery_address', models.CharField(max_length=100)),
                ('pickup_date', models.DateField(blank=True, null=True)),
                ('delivery_date', models.DateField(blank=True, null=True)),
                ('pickup_time', models.TimeField(blank=True, null=True)),
                ('payment_status', models.CharField(default='Pending', max_length=100)),
                ('order_status', models.CharField(default='Initiated', max_length=100)),
                ('complain_status', models.CharField(default='No', max_length=100)),
                ('sender_name', models.CharField(blank=True, max_length=100, null=True)),
                ('sender_email', models.EmailField(blank=True, max_length=254, null=True)),
                ('sender_phone', models.CharField(blank=True, max_length=100, null=True)),
                ('receiver_name', models.CharField(blank=True, max_length=100, null=True)),
                ('receiver_email', models.EmailField(blank=True, max_length=254, null=True)),
                ('receiver_phone', models.CharField(blank=True, max_length=100, null=True)),
                ('description', models.TextField(default='No description provided')),
                ('driver_assigned', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='home.driver')),
            ],
        ),
    ]

# Generated by Django 4.1.5 on 2023-02-02 19:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0009_alter_flight_trip'),
    ]

    operations = [
        migrations.AddField(
            model_name='activity',
            name='date',
            field=models.DateField(blank=True, null=True),
        ),
    ]

# Generated by Django 4.1.5 on 2023-02-08 02:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0015_remove_activity_votes_remove_flight_votes_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='flight',
            name='voted',
            field=models.ManyToManyField(related_name='flights_voted', through='backend.Vote_Status', to='backend.member'),
        ),
    ]
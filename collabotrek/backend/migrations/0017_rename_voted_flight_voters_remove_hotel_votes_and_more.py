# Generated by Django 4.1.5 on 2023-02-08 02:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0016_flight_voted'),
    ]

    operations = [
        migrations.RenameField(
            model_name='flight',
            old_name='voted',
            new_name='voters',
        ),
        migrations.RemoveField(
            model_name='hotel',
            name='votes',
        ),
        migrations.AddField(
            model_name='activity',
            name='voters',
            field=models.ManyToManyField(related_name='activity_voted', through='backend.Vote_Status', to='backend.member'),
        ),
        migrations.AddField(
            model_name='hotel',
            name='voters',
            field=models.ManyToManyField(related_name='hotel_voted', through='backend.Vote_Status', to='backend.member'),
        ),
        migrations.AlterField(
            model_name='vote_status',
            name='activity',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='voted', to='backend.activity'),
        ),
        migrations.AlterField(
            model_name='vote_status',
            name='flight',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='voted', to='backend.flight'),
        ),
        migrations.AlterField(
            model_name='vote_status',
            name='hotel',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='voted', to='backend.hotel'),
        ),
    ]

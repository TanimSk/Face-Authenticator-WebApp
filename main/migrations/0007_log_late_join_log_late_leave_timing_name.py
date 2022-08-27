# Generated by Django 4.1 on 2022-08-27 06:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_alter_timing_time_in_alter_timing_time_out'),
    ]

    operations = [
        migrations.AddField(
            model_name='log',
            name='late_join',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
        migrations.AddField(
            model_name='log',
            name='late_leave',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
        migrations.AddField(
            model_name='timing',
            name='name',
            field=models.CharField(default='main', max_length=20),
        ),
    ]

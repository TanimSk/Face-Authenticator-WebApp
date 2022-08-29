# Generated by Django 4.1 on 2022-08-29 07:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_log_location_in_log_location_out'),
    ]

    operations = [
        migrations.AddField(
            model_name='log',
            name='delay_in',
            field=models.CharField(default='-', max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='log',
            name='delay_out',
            field=models.CharField(default='-', max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='log',
            name='total_hours',
            field=models.CharField(default='-', max_length=20, null=True),
        ),
    ]

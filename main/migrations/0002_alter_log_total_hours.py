# Generated by Django 4.1 on 2022-09-01 10:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='log',
            name='total_hours',
            field=models.CharField(default='-', max_length=50, null=True),
        ),
    ]

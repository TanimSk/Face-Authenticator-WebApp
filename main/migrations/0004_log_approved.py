# Generated by Django 4.1 on 2023-01-05 17:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_delete_timing'),
    ]

    operations = [
        migrations.AddField(
            model_name='log',
            name='approved',
            field=models.BooleanField(blank=True, default=True),
        ),
    ]

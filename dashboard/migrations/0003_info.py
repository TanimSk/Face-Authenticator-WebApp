# Generated by Django 4.1 on 2023-01-05 16:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0002_alter_holiday_month_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Info',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='main', max_length=20)),
                ('geographic_coords', models.CharField(max_length=75)),
                ('radius', models.IntegerField()),
                ('time_in', models.TimeField(blank=True, null=True)),
                ('time_out', models.TimeField(blank=True, null=True)),
            ],
        ),
    ]

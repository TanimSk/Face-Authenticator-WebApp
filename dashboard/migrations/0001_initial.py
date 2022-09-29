# Generated by Django 4.1 on 2022-09-29 05:26

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Holiday',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('month_name', models.CharField(default='-', max_length=100)),
                ('holidays', models.IntegerField(default=0)),
            ],
        ),
    ]

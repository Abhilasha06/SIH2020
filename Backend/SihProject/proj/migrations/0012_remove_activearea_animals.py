# Generated by Django 3.0.6 on 2020-07-24 22:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('proj', '0011_auto_20200724_2146'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='activearea',
            name='animals',
        ),
    ]

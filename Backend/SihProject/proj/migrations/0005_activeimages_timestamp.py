# Generated by Django 3.0.6 on 2020-07-12 22:47

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('proj', '0004_auto_20200712_1813'),
    ]

    operations = [
        migrations.AddField(
            model_name='activeimages',
            name='timestamp',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]

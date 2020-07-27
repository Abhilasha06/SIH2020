# Generated by Django 3.0.6 on 2020-07-26 23:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('proj', '0016_auto_20200725_1154'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='activearea',
            name='ngoName',
        ),
        migrations.RemoveField(
            model_name='appuser',
            name='contributionImages',
        ),
        migrations.AddField(
            model_name='activeimages',
            name='contributing_user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='activeimages',
            name='area',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='proj.ActiveArea'),
        ),
    ]
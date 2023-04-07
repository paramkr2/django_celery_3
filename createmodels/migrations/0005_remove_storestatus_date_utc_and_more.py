# Generated by Django 4.1.4 on 2023-04-05 20:17

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('createmodels', '0004_businesshours_storetimezone'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='storestatus',
            name='date_utc',
        ),
        migrations.RemoveField(
            model_name='storestatus',
            name='time_utc',
        ),
        migrations.AddField(
            model_name='storestatus',
            name='datetime_utc',
            field=models.DateTimeField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
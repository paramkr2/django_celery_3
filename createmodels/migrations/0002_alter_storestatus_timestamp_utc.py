# Generated by Django 4.1.4 on 2023-04-02 15:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('createmodels', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='storestatus',
            name='timestamp_utc',
            field=models.DateField(),
        ),
    ]

# Generated by Django 4.0.3 on 2023-02-14 08:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_device_group'),
    ]

    operations = [
        migrations.AddField(
            model_name='device',
            name='status',
            field=models.BooleanField(default=False),
        ),
    ]

# Generated by Django 3.0.4 on 2020-04-01 18:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scripts', '0002_auto_20200330_1500'),
    ]

    operations = [
        migrations.AddField(
            model_name='process',
            name='status_msg',
            field=models.TextField(blank=True),
        ),
    ]

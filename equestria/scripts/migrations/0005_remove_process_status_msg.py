# Generated by Django 3.0.4 on 2020-04-02 05:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scripts', '0004_logmessage'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='process',
            name='status_msg',
        ),
    ]

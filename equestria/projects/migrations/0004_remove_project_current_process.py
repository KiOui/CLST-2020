# Generated by Django 3.1.4 on 2020-12-27 18:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0003_auto_20201226_2330'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='project',
            name='current_process',
        ),
    ]

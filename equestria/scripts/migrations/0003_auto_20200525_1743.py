# Generated by Django 3.0.6 on 2020-05-25 15:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scripts', '0002_auto_20200520_2100'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='project',
            options={'permissions': [('access_project', 'Access project')]},
        ),
    ]
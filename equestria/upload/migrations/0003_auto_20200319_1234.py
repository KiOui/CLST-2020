# Generated by Django 3.0.4 on 2020-03-19 11:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('upload', '0002_auto_20200319_1154'),
    ]

    operations = [
        migrations.AlterField(
            model_name='file',
            name='owner',
            field=models.CharField(max_length=30),
        ),
    ]
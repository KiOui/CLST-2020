# Generated by Django 3.0.4 on 2020-03-25 08:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('script_runner', '0012_auto_20200324_2009'),
    ]

    operations = [
        migrations.AddField(
            model_name='process',
            name='output_path',
            field=models.CharField(default='output/error.log', max_length=512),
        ),
    ]
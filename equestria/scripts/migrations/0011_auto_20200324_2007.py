# Generated by Django 3.0.4 on 2020-03-24 20:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('script_runner', '0010_auto_20200324_2006'),
    ]

    operations = [
        migrations.AlterField(
            model_name='process',
            name='output_file',
            field=models.CharField(blank=True, default='', max_length=512, null=True),
        ),
    ]

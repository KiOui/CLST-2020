# Generated by Django 3.0.4 on 2020-03-18 13:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('script_runner', '0004_inputtemplate_mime'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inputtemplate',
            name='mime',
            field=models.CharField(default='text/plain', max_length=1024),
        ),
    ]

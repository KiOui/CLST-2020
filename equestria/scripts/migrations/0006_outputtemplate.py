# Generated by Django 3.1.4 on 2021-01-02 10:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scripts', '0005_auto_20210101_1745'),
    ]

    operations = [
        migrations.CreateModel(
            name='OutputTemplate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=1024)),
                ('regex', models.CharField(max_length=1024)),
            ],
        ),
    ]

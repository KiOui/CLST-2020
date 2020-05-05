# Generated by Django 3.0.4 on 2020-04-22 13:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('scripts', '0012_auto_20200421_1156'),
    ]

    operations = [
        migrations.CreateModel(
            name='BaseParameter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=1024)),
                ('preset', models.BooleanField(default=False)),
                ('corresponding_script', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='scripts.Script')),
            ],
        ),
        migrations.CreateModel(
            name='StringParameter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(max_length=2048)),
                ('relation', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='scripts.BaseParameter')),
            ],
        ),
        migrations.CreateModel(
            name='ChoiceParameter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(max_length=2048)),
                ('relation', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='scripts.BaseParameter')),
            ],
        ),
        migrations.CreateModel(
            name='BooleanParameter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.BooleanField(default=False)),
                ('relation', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='scripts.BaseParameter')),
            ],
        ),
    ]
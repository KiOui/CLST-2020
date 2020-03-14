# Generated by Django 3.0.3 on 2020-03-14 15:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('script_runner', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Process',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=512)),
                ('clam_id', models.CharField(max_length=256)),
            ],
            options={
                'verbose_name_plural': 'Scripts',
                'ordering': ['name'],
            },
        ),
        migrations.AlterField(
            model_name='outputfile',
            name='output_file',
            field=models.FilePathField(path='./'),
        ),
        migrations.AlterField(
            model_name='script',
            name='output_file_or_directory',
            field=models.FilePathField(allow_folders=True, blank=True, help_text='Additional outputs generated', path='./'),
        ),
        migrations.AlterField(
            model_name='script',
            name='primary_output_file',
            field=models.FilePathField(blank=True, help_text='The file to be used for live output', path='./'),
        ),
        migrations.AlterField(
            model_name='script',
            name='script_file',
            field=models.FilePathField(blank=True, help_text='specify either a file to execute', path='./'),
        ),
        migrations.CreateModel(
            name='InputFile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=512)),
                ('input_file', models.FilePathField(path='uploads/')),
                ('description', models.TextField(max_length=32768)),
                ('associated_process', models.ManyToManyField(default=None, to='script_runner.Process')),
            ],
        ),
    ]
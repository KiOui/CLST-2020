# Generated by Django 3.1.5 on 2021-01-06 09:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('projects', '0001_initial'),
        ('scripts', '0003_auto_20210106_1056'),
    ]

    operations = [
        migrations.CreateModel(
            name='Process',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('clam_id', models.CharField(default=None, max_length=256, null=True)),
                ('status', models.IntegerField(choices=[(0, 'Created'), (1, 'Uploading files to CLAM'), (2, 'Running'), (3, 'Waiting for download from CLAM'), (4, 'Downloading files from CLAM'), (5, 'Finished'), (-1, 'Error'), (-2, 'Error while downloading files from CLAM')], default=0)),
                ('folder', models.FilePathField(allow_files=False, allow_folders=True, path='media/processes')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projects.project')),
                ('script', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='scripts.script')),
            ],
            options={
                'verbose_name_plural': 'Processes',
            },
        ),
        migrations.CreateModel(
            name='LogMessage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.DateTimeField(null=True)),
                ('message', models.CharField(max_length=16384)),
                ('index', models.PositiveIntegerField()),
                ('process', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='processes.process')),
            ],
        ),
        migrations.CreateModel(
            name='FileSetting',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projects.file')),
                ('input_template', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='file_settings', to='scripts.inputtemplate')),
            ],
        ),
        migrations.CreateModel(
            name='FilePreset',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=1024)),
                ('regex', models.CharField(max_length=1024)),
                ('input_template', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='scripts.inputtemplate')),
            ],
        ),
        migrations.CreateModel(
            name='ParameterSetting',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('_value', models.CharField(max_length=1024)),
                ('base_parameter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='parameter_setting', to='scripts.baseparameter')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projects.project')),
            ],
            options={
                'unique_together': {('base_parameter', 'project')},
            },
        ),
    ]

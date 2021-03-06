# Generated by Django 3.1.5 on 2021-01-20 12:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import projects.models


class Migration(migrations.Migration):

    dependencies = [
        ('pipelines', '0002_auto_20210120_1353'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('projects', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='file',
            name='file',
            field=models.FileField(help_text='The file.', unique=True, upload_to=projects.models.project_folder_path),
        ),
        migrations.AlterField(
            model_name='file',
            name='project',
            field=models.ForeignKey(help_text='The Project this file belongs to.', on_delete=django.db.models.deletion.CASCADE, to='projects.project'),
        ),
        migrations.AlterField(
            model_name='project',
            name='name',
            field=models.CharField(help_text='The name of the Project.', max_length=512),
        ),
        migrations.AlterField(
            model_name='project',
            name='pipeline',
            field=models.ForeignKey(help_text='The Pipeline this Project belongs to.', on_delete=django.db.models.deletion.CASCADE, to='pipelines.pipeline'),
        ),
        migrations.AlterField(
            model_name='project',
            name='user',
            field=models.ForeignKey(help_text='The User this Project belongs to.', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]

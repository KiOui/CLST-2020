# Generated by Django 3.1.4 on 2021-01-01 16:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0004_remove_project_current_process'),
        ('scripts', '0005_auto_20210101_1745'),
        ('processes', '0002_auto_20201228_0942'),
    ]

    operations = [
        migrations.AddField(
            model_name='process',
            name='project',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='projects.project'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='parametersetting',
            name='base_parameter',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='parameter_setting', to='scripts.baseparameter'),
        ),
    ]

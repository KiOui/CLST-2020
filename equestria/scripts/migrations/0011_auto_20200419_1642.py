# Generated by Django 3.0.4 on 2020-04-19 16:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scripts', '0010_auto_20200418_1102'),
    ]

    operations = [
        migrations.AlterField(
            model_name='process',
            name='folder',
            field=models.FilePathField(allow_files=False, allow_folders=True, path='/home/david/Desktop/CLST-2020/CLST-2020/equestria/userdata'),
        ),
        migrations.AlterField(
            model_name='project',
            name='folder',
            field=models.FilePathField(allow_files=False, allow_folders=True, path='/home/david/Desktop/CLST-2020/CLST-2020/equestria/userdata'),
        ),
    ]
# Generated by Django 3.0.4 on 2020-04-01 19:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("scripts", "0003_process_status_msg"),
    ]

    operations = [
        migrations.CreateModel(
            name="LogMessage",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("time", models.DateTimeField()),
                ("message", models.CharField(max_length=16384)),
                ("index", models.PositiveIntegerField()),
                (
                    "process",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="scripts.Process",
                    ),
                ),
            ],
        ),
    ]
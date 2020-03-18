from django.db import models
from equestria.settings import BASE_DIR
import os
from django.contrib.auth.models import User

# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Create your models here.
class File(models.Model):
    owner = models.ForeignKey(
        User, to_field="username", on_delete=models.CASCADE
    )
    timestamp = models.DateTimeField(auto_now_add=True)
    path = models.FilePathField(path=os.path.join(BASE_DIR, "media/"))

    def __str__(self):
        """Use name of script in admin display."""
        return self.name

    class Meta:
        """
        Display configuration for admin pane.

        Display plural correctly.
        """

        verbose_name_plural = "Files"


# python manage.py makemigrations
# python manage.py migrate

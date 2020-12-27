from django.db import models
from scripts.models import Script


class Pipeline(models.Model):
    """Pipeline model class."""

    name = models.CharField(max_length=512)
    fa_script = models.ForeignKey(
        Script,
        on_delete=models.PROTECT,
        blank=False,
        null=False,
        related_name="fa_script",
    )
    g2p_script = models.ForeignKey(
        Script,
        on_delete=models.PROTECT,
        blank=False,
        null=False,
        related_name="g2p_script",
    )

    def __str__(self):
        """
        Convert this object to a string.

        :return: the name property of this object
        """
        return self.name

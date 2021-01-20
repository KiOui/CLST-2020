from django.db import models
from scripts.models import Script


class Pipeline(models.Model):
    """Pipeline model class."""

    name = models.CharField(
        max_length=512,
        help_text="The name of the Pipeline to appear to users when creating a new Project.",
    )
    fa_script = models.ForeignKey(
        Script,
        on_delete=models.PROTECT,
        blank=False,
        null=False,
        related_name="fa_script",
        help_text="The Forced Alignment Script to use for the Forced Alignment part of the Pipeline.",
    )
    g2p_script = models.ForeignKey(
        Script,
        on_delete=models.PROTECT,
        blank=False,
        null=False,
        related_name="g2p_script",
        help_text="The Grapheme to Phoneme Script to use for the Grapheme to Phoneme part of the Pipeline.",
    )

    def __str__(self):
        """
        Convert this object to a string.

        :return: the name property of this object
        """
        return self.name

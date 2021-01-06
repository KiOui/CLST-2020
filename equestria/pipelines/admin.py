from django.contrib import admin
from pipelines import models


@admin.register(models.Pipeline)
class PipelineAdmin(admin.ModelAdmin):
    """Model admin for Pipelines."""

    list_display = ["name", "fa_script", "g2p_script"]

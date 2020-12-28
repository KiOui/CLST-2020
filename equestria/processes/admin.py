from django.contrib import admin
from processes import models


@admin.register(models.Process)
class ProcessAdmin(admin.ModelAdmin):
    """Model admin for Processes."""

    list_display = ["folder", "script", "status"]
    list_filter = ["status", "script"]


@admin.register(models.FileSetting)
class FileSettingsAdmin(admin.ModelAdmin):
    """Model admin for File settings."""

    list_display = ["file", "input_template"]


@admin.register(models.ParameterSetting)
class ParameterSettingsAdmin(admin.ModelAdmin):
    """Model admin for Parameter settings."""

    list_display = ["value", "base_parameter"]

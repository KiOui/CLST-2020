from django.contrib import admin
from processes import models
from processes.forms import FilePresetAdminForm


@admin.register(models.Process)
class ProcessAdmin(admin.ModelAdmin):
    """Model admin for Processes."""

    list_display = ["id", "project", "script", "status"]
    list_filter = ["status", "script", "project"]


@admin.register(models.FileSetting)
class FileSettingsAdmin(admin.ModelAdmin):
    """Model admin for File settings."""

    list_display = ["file", "input_template"]


@admin.register(models.ParameterSetting)
class ParameterSettingsAdmin(admin.ModelAdmin):
    """Model admin for Parameter settings."""

    list_display = ["value", "base_parameter"]


@admin.register(models.FilePreset)
class FilePresetAdmin(admin.ModelAdmin):
    """Model admin for File presets."""

    form = FilePresetAdminForm

    list_display = ["name", "input_template", "regex"]

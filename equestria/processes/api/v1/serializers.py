from processes.models import FileSetting, ParameterSetting
from rest_framework import serializers
from scripts.models import Script, Profile, InputTemplate, BaseParameter
from processes import models


class ParameterSettingSerializer(serializers.ModelSerializer):
    """Serializer for File model."""

    class Meta:
        """Meta class."""

        model = models.ParameterSetting
        fields = [
            "value",
        ]


class ParameterSerializer(serializers.ModelSerializer):
    """Serializer for Parameter model."""
    parameter_setting = serializers.SerializerMethodField()

    def get_parameter_setting(self, instance):
        try:
            parameter_setting = ParameterSetting.objects.get(base_parameter=instance, project=self.context.get('view').kwargs.get('project'))
        except ParameterSetting.DoesNotExist:
            parameter_setting = None
        return ParameterSettingSerializer(parameter_setting, many=False).data

    class Meta:
        """Meta class."""

        model = BaseParameter
        fields = [
            "name",
            "parameter_setting",
        ]


class FileSettingSerializer(serializers.ModelSerializer):
    """Serializer for File model."""

    class Meta:
        """Meta class."""

        model = models.FileSetting
        fields = [
            "file",
        ]


class InputTemplateSettingSerializer(serializers.ModelSerializer):
    """Serializer for input template settings."""
    file_settings = serializers.SerializerMethodField()

    def get_file_settings(self, instance):
        return FileSettingSerializer(FileSetting.objects.filter(input_template=instance, file__project=self.context.get('view').kwargs.get('project')), many=True).data

    class Meta:
        """Meta class."""

        model = InputTemplate
        fields = [
            "id",
            "file_settings",
        ]


class ProfileSettingSerializer(serializers.ModelSerializer):
    """Serializer for profile settings."""
    input_templates = InputTemplateSettingSerializer(many=True, read_only=True)

    class Meta:
        """Meta class."""

        model = Profile
        fields = [
            "id",
            "input_templates",
        ]


class SettingsSerializer(serializers.ModelSerializer):
    """Serializer for Product model."""
    profiles = ProfileSettingSerializer(many=True, read_only=True)
    parameters = ParameterSerializer(many=True, read_only=True)

    class Meta:
        """Meta class."""

        model = Script
        fields = [
            "profiles",
            "parameters",
        ]

from processes.models import FileSetting, ParameterSetting
from rest_framework import serializers
from scripts.models import Script, Profile, InputTemplate, BaseParameter
from processes import models


class ParameterSerializer(serializers.ModelSerializer):
    """Serializer for Parameter model."""
    value = serializers.SerializerMethodField()

    def get_value(self, instance):
        try:
            return ParameterSetting.objects.get(base_parameter=instance, project=self.context.get('view').kwargs.get('project')).value
        except ParameterSetting.DoesNotExist:
            return None

    @property
    def validated_data(self):
        print(self.data)
        print(super().validated_data)
        return super().validated_data

    class Meta:
        """Meta class."""

        model = BaseParameter
        fields = [
            "name",
            "value",
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
    files = serializers.SerializerMethodField()

    def get_files(self, instance):
        return [x.file.id for x in FileSetting.objects.filter(input_template=instance, file__project=self.context.get('view').kwargs.get('project'))]

    class Meta:
        """Meta class."""

        model = InputTemplate
        fields = [
            "id",
            "files",
        ]


class ProfileSettingSerializer(serializers.ModelSerializer):
    """Serializer for profile settings."""
    input_templates = InputTemplateSettingSerializer(many=True, read_only=False)

    class Meta:
        """Meta class."""

        model = Profile
        fields = [
            "id",
            "input_templates",
        ]


class SettingsSerializer(serializers.ModelSerializer):
    """Serializer for Product model."""
    profiles = ProfileSettingSerializer(many=True, read_only=False)
    parameters = ParameterSerializer(many=True, read_only=False)

    class Meta:
        """Meta class."""

        model = Script
        fields = [
            "profiles",
            "parameters",
        ]

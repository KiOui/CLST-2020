from processes.models import FileSetting, ParameterSetting, Process, LogMessage
from rest_framework import serializers
from scripts.models import Script, Profile, InputTemplate, BaseParameter
from processes import models


class LogMessageSerializer(serializers.ModelSerializer):
    """Serializer for LogMessage model."""

    class Meta:
        """Meta class."""

        model = LogMessage
        fields = [
            "index",
            "message",
            "time",
        ]


class ProcessSerializer(serializers.ModelSerializer):
    """Serializer for Process model."""

    log_messages = serializers.SerializerMethodField()
    status_string = serializers.SerializerMethodField()
    script_type = serializers.SerializerMethodField()

    def get_log_messages(self, instance):
        return LogMessageSerializer(instance.log_messages, many=True).data

    def get_script_type(self, instance):
        return "FA" if instance.script == instance.project.pipeline.fa_script else "G2P"

    def get_status_string(self, instance):
        return instance.get_status_string()

    class Meta:
        """Meta class."""

        model = Process
        fields = [
            "pk",
            "script",
            "script_type",
            "project",
            "status",
            "status_string",
            "log_messages",
            "created",
        ]


class ParameterSerializer(serializers.ModelSerializer):
    """Serializer for Parameter model."""
    value = serializers.SerializerMethodField()

    def get_value(self, instance):
        try:
            return ParameterSetting.objects.get(base_parameter=instance, project=self.context.get('view').kwargs.get('project')).raw_value
        except ParameterSetting.DoesNotExist:
            return None

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

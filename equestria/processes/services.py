from projects.models import File
from scripts.models import BaseParameter, Profile, InputTemplate

from .models import ParameterSetting, FileSetting


class InputTemplateSettingParser:

    def __init__(self, input_template_id, files):
        self.input_template_id = input_template_id
        self.files = files

    @staticmethod
    def parse(input_template):
        if type(input_template) == dict and "id" in input_template.keys() and "files" in input_template.keys():
            if type(input_template["id"]) == int and type(input_template["files"]) == list:
                input_template_id = input_template["id"]
                files = [x for x in input_template["files"] if type(x) == int]
                return InputTemplateSettingParser(input_template_id, files)
        return None

    def to_dict(self):
        return {"id": self.input_template_id, "files": self.files}

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return self.to_dict().__str__()


class ProfileSettingParser:

    def __init__(self, profile_id, input_templates):
        self.profile_id = profile_id
        self.input_templates = input_templates

    @staticmethod
    def parse(profile):
        if type(profile) == dict and "id" in profile.keys() and "input_templates" in profile.keys():
            if type(profile["id"]) == int and type(profile["input_templates"]) == list:
                profile_id = profile["id"]
                input_templates = [x for x in [InputTemplateSettingParser.parse(x) for x in profile["input_templates"]] if x is not None]
                return ProfileSettingParser(profile_id, input_templates)
        return None

    def to_dict(self):
        return {"id": self.profile_id, "input_templates": self.input_templates}

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return self.to_dict().__str__()


class ParameterSettingParser:

    def __init__(self, name, value):
        self.name = name
        self.value = value

    @staticmethod
    def parse(parameter):
        if type(parameter) == dict and "name" in parameter.keys() and "value" in parameter.keys():
            if type(parameter["name"]) == str and type(parameter["value"]) == str:
                return ParameterSettingParser(parameter["name"], parameter["value"])
            elif type(parameter["name"]) == str and type(parameter["value"]) == bool:
                return ParameterSettingParser(parameter["name"], str(parameter["value"]))
        return None

    def to_dict(self):
        return {"name": self.name, "value": self.value}

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return self.to_dict().__str__()


def parse_profiles(profiles):
    print(profiles)
    if type(profiles) == list:
        return [x for x in [ProfileSettingParser.parse(x) for x in profiles] if x is not None]
    else:
        return []


def parse_parameters(parameters):
    if type(parameters) == list:
        return [x for x in [ParameterSettingParser.parse(x) for x in parameters] if x is not None]
    else:
        return []


def handle_parameter_changing(parameters: [ParameterSettingParser], project, script):
    parameters_altered = list()
    for parameter in parameters:
        try:
            base_parameter_obj = BaseParameter.objects.get(corresponding_script=script, name=parameter.name)
            if ParameterSetting.objects.filter(project=project, base_parameter=base_parameter_obj).exists():
                try:
                    parameter_setting = ParameterSetting.objects.get(project=project, base_parameter=base_parameter_obj)
                    parameter_setting._value = parameter.value
                    parameter_setting.save()
                    parameters_altered.append(parameter_setting)
                except ParameterSetting.InvalidValueType:
                    pass
            else:
                try:
                    parameters_altered.append(ParameterSetting.objects.create(project=project, base_parameter=base_parameter_obj, _value=parameter.value))
                except ParameterSetting.InvalidValueType:
                    pass
        except BaseParameter.DoesNotExist:
            pass
    return parameters_altered


def handle_profile_changing(profiles: [ProfileSettingParser], project, script):
    files_altered = list()
    for profile in profiles:
        try:
            profile_obj = Profile.objects.get(pk=profile.profile_id, script=script)
            for input_template in profile.input_templates:
                try:
                    input_template_obj = InputTemplate.objects.get(pk=input_template.input_template_id, corresponding_profile=profile_obj)
                    for file in input_template.files:
                        try:
                            file_obj = File.objects.get(project=project, pk=file)
                            file_setting, _ = FileSetting.objects.get_or_create(input_template=input_template_obj, file=file_obj)
                            files_altered.append(file_setting)
                        except File.DoesNotExist:
                            pass
                except InputTemplate.DoesNotExist:
                    pass
        except Profile.DoesNotExist:
            pass
    return files_altered


def autoconfigure_file_settings(project, script):
    FileSetting.objects.filter(file__project=project, input_template__corresponding_profile__script=script).delete()
    for input_template in InputTemplate.objects.filter(corresponding_profile__script=script):
        FileSetting.create_for_input_template(input_template, project)


def check_process_ready(project, script, profile):
    errors = []
    input_templates = InputTemplate.objects.filter(corresponding_profile=profile)
    for template in input_templates:
        file_settings_amount = FileSetting.objects.filter(file__project=project, input_template=template).count()
        if template.optional and template.unique and file_settings_amount > 1:
            errors.append("Template '{}' requires a unique file but multiple were specified.".format(template.label))
        elif not template.optional and template.unique and file_settings_amount != 1:
            errors.append("Template '{}' requires a unique file but {} were specified.".format(template.label, file_settings_amount))
        elif not template.optional and not template.unique and file_settings_amount < 1:
            errors.append("Template '{}' requires a file but none were specified".format(template.label))

    for parameter in script.variable_parameters:
        try:
            ParameterSetting.objects.get(project=project, base_parameter=parameter)
        except ParameterSetting.DoesNotExist:
            errors.append("Parameter '{}' requires a value but none is given.".format(parameter))
    return errors


def find_ready_profiles(project, script):
    profiles_ready = []
    for profile in Profile.objects.filter(script=script):
        errors = check_process_ready(project, script, profile)
        if len(errors) == 0:
            profiles_ready.append(profile)
    return profiles_ready
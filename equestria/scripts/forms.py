"""Module to define forms related to the scripts app."""
import re

from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

from .models import Profile, BaseParameter, OutputTemplate
from .models import ChoiceParameter, Choice

User = get_user_model()


class ProfileSelectForm(forms.Form):
    """Form for running a profile."""

    profile = forms.ChoiceField(choices=[])

    def __init__(self, *args, **kwargs):
        """
        Initialise method for ProfileSelectForm.

        :param args: argument
        :param kwargs: keyword arguments containing a scripts variable with Script objects
        """
        profiles = kwargs.pop("profiles", None)
        super(ProfileSelectForm, self).__init__(*args, **kwargs)
        choices = []
        if profiles is not None:
            for p in profiles:
                choices.append((p.id, "Profile {}".format(p.id)))
            self.fields["profile"].choices = choices

    def clean_profile(self):
        """
        Clean the profile variable in this form.

        :return: the cleaned profile variable
        """
        profile = self.cleaned_data.get("profile")
        profile_qs = Profile.objects.filter(id=profile)
        if not profile_qs.exists():
            raise forms.ValidationError("This profile does not exist")

        return profile


class AlterDictionaryForm(forms.Form):
    """Form for altering the dictionary."""

    dictionary = forms.CharField(
        widget=forms.Textarea(attrs={"style": "width: 100%;"}),
        required=False,
        label=False,
    )


class ParameterForm(forms.Form):
    """Form for setting parameters."""

    def __init__(self, parameters, *args, **kwargs):
        """
        Initialise the ParameterForm.

        :param parameters: a list of BaseParameter objects including the parameters to add to this form, field types are
        automatically set for the parameters
        :param args: arguments
        :param kwargs: keyword arguments
        """
        super(ParameterForm, self).__init__(*args, **kwargs)
        for parameter in parameters:
            if parameter.type == BaseParameter.BOOLEAN_TYPE:
                self.fields[parameter.name] = forms.BooleanField()
            elif parameter.type == BaseParameter.STATIC_TYPE:
                self.fields[parameter.name] = forms.CharField(
                    widget=forms.HiddenInput(),
                    initial=parameter.get_default_value(),
                )
            elif parameter.type == BaseParameter.STRING_TYPE:
                self.fields[parameter.name] = forms.CharField()
            elif parameter.type == BaseParameter.CHOICE_TYPE:
                self.fields[parameter.name] = forms.ChoiceField(choices=[])
                choice_parameter = ChoiceParameter.objects.get(base=parameter)
                choices = list()
                for choice in Choice.objects.filter(
                    corresponding_choice_parameter=choice_parameter
                ):
                    choices.append((choice.value, choice.value))
                self.fields[parameter.name].choices = choices
            elif parameter.type == BaseParameter.TEXT_TYPE:
                self.fields[parameter.name] = forms.CharField(
                    widget=forms.Textarea
                )
            elif parameter.type == BaseParameter.INTEGER_TYPE:
                self.fields[parameter.name] = forms.IntegerField()
            elif parameter.type == BaseParameter.FLOAT_TYPE:
                self.fields[parameter.name] = forms.FloatField()


class ChoiceParameterAdminForm(forms.ModelForm):
    """Admin form for ChoiceParameter."""

    class Meta:
        """Meta class."""

        model = ChoiceParameter
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        """
        Initialise the ChoiceParameterAdminForm.

        This method restricts the choices on the 'value' field in the admin form to choices that correspond to the
        ChoiceParameter object.
        :param args: arguments
        :param kwargs: keyword arguments
        """
        super(ChoiceParameterAdminForm, self).__init__(*args, **kwargs)
        if self.instance:
            self.fields["value"].queryset = Choice.objects.filter(
                corresponding_choice_parameter=self.instance
            )


class OutputTemplateAdminForm(forms.ModelForm):
    """Admin form for OutputTemplate."""

    def clean_regex(self):
        regex = self.cleaned_data.get("regex")
        try:
            re.compile(regex)
            return regex
        except re.error as e:
            raise ValidationError("The regex is incorrect and returned the following error: {}".format(e))

    class Meta:
        """Meta class."""

        model = OutputTemplate
        fields = "__all__"

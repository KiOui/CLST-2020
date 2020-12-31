from processes.api.v1.serializers import SettingsSerializer
from processes.models import FileSetting, ParameterSetting
from projects.api.v1.permissions import IsOwner
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from scripts.models import Script
from processes.services import parse_profiles, parse_parameters, handle_parameter_changing, handle_profile_changing, \
    autoconfigure_file_settings


class ScriptSettingsRetrieveUpdateAPIView(RetrieveUpdateAPIView):

    serializer_class = SettingsSerializer
    queryset = Script.objects.all()
    owner_key = "user"
    permission_classes = [IsAuthenticated, IsOwner]

    def get_permissions_object(self):
        """Get permission object."""
        return self.kwargs.get("project")

    def get_queryset(self):
        script_list = [self.kwargs.get("project").pipeline.fa_script.pk, self.kwargs.get("project").pipeline.g2p_script.pk]
        return self.queryset.filter(pk__in=script_list)

    def update_parameters_and_profiles(self, project, script):
        files_altered = []
        parameters_altered = []
        if 'profiles' in self.request.data.keys():
            files_altered = handle_profile_changing(parse_profiles(self.request.data["profiles"]), project, script)
        if 'parameters' in self.request.data.keys():
            parameters_altered = handle_parameter_changing(parse_parameters(self.request.data["parameters"]), project,
                                                           script)
        return files_altered, parameters_altered

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        project = self.kwargs.get("project")
        script = Script.objects.get(pk=self.kwargs.get('pk'))
        if project.pipeline.fa_script == script or project.pipeline.g2p_script == script:
            files_altered, parameters_altered = self.update_parameters_and_profiles(project, script)
            if not partial:
                ParameterSetting.objects.filter(project=project).exclude(
                    pk__in=[x.pk for x in parameters_altered]).delete()
                FileSetting.objects.filter(file__project=project).exclude(
                    pk__in=[x.pk for x in files_altered]).delete()
            return self.retrieve(request, *args, **kwargs)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(["POST"])
def configure_automatically(request, **kwargs):
    """Configure input templates automatically."""
    project = kwargs.get("project")
    script = kwargs.get("script")
    if request.user.is_authenticated and request.user == project.user:
        if script == project.pipeline.fa_script or script == project.pipeline.g2p_script:
            autoconfigure_file_settings(project, script)
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)
    else:
        raise PermissionDenied

from processes.api.v1.serializers import SettingsSerializer
from projects.api.v1.permissions import IsOwner
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated
from scripts.models import Script


class ScriptSettingsRetrieveUpdateAPIView(RetrieveUpdateAPIView):

    serializer_class = SettingsSerializer
    queryset = Script.objects.all()
    owner_key = "user"
    permission_classes = [IsAuthenticated, IsOwner]

    def get_permissions_object(self):
        """Get permission object."""
        return self.kwargs.get("project")

    def update(self, request, *args, **kwargs):
        super().update(request, *args, **kwargs)

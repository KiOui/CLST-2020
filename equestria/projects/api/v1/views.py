from projects.api.v1.permissions import IsOwner
from projects.models import Project, File
from rest_framework import mixins, viewsets, status
from rest_framework.decorators import api_view
from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import (
    ListAPIView,
    DestroyAPIView,
    ListCreateAPIView,
    RetrieveDestroyAPIView,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .serializers import ProjectSerializer, FileSerializer


class FileListCreateView(ListCreateAPIView):
    """File API view for listing and creating."""

    serializer_class = FileSerializer
    owner_key = "user"
    permission_classes = [IsAuthenticated, IsOwner]
    queryset = File.objects.all()

    def perform_create(self, serializer):
        """Create a File."""
        serializer.save(project=self.kwargs.get("project"))

    def get_queryset(self):
        """Get queryset."""
        return self.queryset.filter(project=self.kwargs.get("project"))

    def get_permissions_object(self):
        """Get permission object."""
        return self.kwargs.get("project")


class FileRetrieveDestroyView(RetrieveDestroyAPIView):
    """File API view for retrieving and destroying."""

    serializer_class = FileSerializer
    owner_key = "user"
    permission_classes = [IsAuthenticated, IsOwner]
    queryset = File.objects.all()

    def get_queryset(self):
        """Get queryset."""
        return self.queryset.filter(project=self.kwargs.get("project"))

    def get_permissions_object(self):
        """Get permission object."""
        return self.kwargs.get("project")


class ProjectListCreateView(ListCreateAPIView):
    """Project API view for listing and creating."""

    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]
    queryset = Project.objects.all()

    def get_queryset(self):
        """Get queryset."""
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        """Create a Project."""
        serializer.save(user=self.request.user)


class ProjectRetrieveDestroyView(RetrieveDestroyAPIView):
    """Project API view for retrieving and destroying."""

    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]
    queryset = Project.objects.all()

    def get_queryset(self):
        """Get queryset."""
        return self.queryset.filter(user=self.request.user)


@api_view(["POST"])
def project_clear_files(request, **kwargs):
    """Clear a project folder."""
    project = kwargs.get("project")
    if request.user.is_authenticated and request.user == project.user:
        project.clear_project_folder()
        return Response(status=status.HTTP_200_OK)
    else:
        raise PermissionDenied

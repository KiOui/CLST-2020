from django.urls import path, register_converter
from projects.api.v1.views import (
    ProjectListCreateView,
    FileListCreateView,
    FileRetrieveDestroyView,
    ProjectRetrieveDestroyView,
    project_clear_files,
)
from projects.converters import ProjectConverter


register_converter(ProjectConverter, "project")

urlpatterns = [
    path("", ProjectListCreateView.as_view(), name="project-listcreate"),
    path(
        "<int:pk>/",
        ProjectRetrieveDestroyView.as_view(),
        name="project-retrievedestroy",
    ),
    path(
        "<project:project>/files/",
        FileListCreateView.as_view(),
        name="project-file-listcreate",
    ),
    path(
        "<project:project>/files/<int:pk>/",
        FileRetrieveDestroyView.as_view(),
        name="project-file-retrievedestroy",
    ),
    path(
        "<project:project>/files/clear/",
        project_clear_files,
        name="project-file-clear",
    ),
]

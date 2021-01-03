"""Module to parse URL and direct accordingly."""
from django.urls import path, register_converter
from .views import *
from .converters import (
    ProfileConverter,
    ScriptConverter,
)
from projects.converters import ProjectConverter

register_converter(ProjectConverter, "project")
register_converter(ProfileConverter, "profile")
register_converter(ScriptConverter, "script")

urlpatterns = [
    path(
        "projects/<project:project>/delete",
        ProjectDeleteView.as_view(),
        name="delete_project",
    ),
    path(
        "project/<project:project>/download",
        download_project_archive,
        name="project_download",
    ),
]

from django.urls import path, register_converter
from processes.api.v1.views import (
    ScriptSettingsRetrieveUpdateAPIView
)
from projects.converters import ProjectConverter


register_converter(ProjectConverter, "project")


urlpatterns = [
    path(
        "settings/<project:project>/<int:pk>/",
        ScriptSettingsRetrieveUpdateAPIView.as_view(),
        name="script-settings",
    ),
]

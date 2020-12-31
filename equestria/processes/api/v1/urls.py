from django.urls import path, register_converter
from processes.api.v1.views import (
    ScriptSettingsRetrieveUpdateAPIView, configure_automatically
)
from scripts.converters import ScriptConverter
from projects.converters import ProjectConverter


register_converter(ProjectConverter, "project")
register_converter(ScriptConverter, "script")


urlpatterns = [
    path(
        "settings/<project:project>/<int:pk>/",
        ScriptSettingsRetrieveUpdateAPIView.as_view(),
        name="script-settings",
    ),
    path(
        "settings/<project:project>/<script:script>/configure-automatically",
        configure_automatically,
        name="configure-automatically",
    ),
]

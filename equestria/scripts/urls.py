from django.urls import path
from scripts.views import *

urlpatterns = [
    path("process/<int:process>", ProcessOverview.as_view(), name="process"),
    path("fa/", FAView.as_view(), name="FA_form"),
    path(
        "fa/<int:process>",
        ForcedAlignmentProjectDetails.as_view(),
        name="fa_project",
    ),
    path(
        "process/<int:process>/status",
        JsonProcess.as_view(),
        name="process_details",
    ),
    path(
        "process/<int:process>/download",
        download_process_archive,
        name="process_download",
    ),
]

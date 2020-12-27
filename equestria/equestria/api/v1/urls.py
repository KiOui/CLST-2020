from django.urls import path, include

app_name = "equestria"

urlpatterns = [
    path("projects/", include("projects.api.v1.urls")),
]

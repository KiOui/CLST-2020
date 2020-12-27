from django.contrib import admin
from django.urls import include, path
from equestria.views import WelcomePage

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", WelcomePage.as_view(), name="welcome"),
    path(
        "scripts/", include(("scripts.urls", "scripts"), namespace="scripts"),
    ),
    path(
        "projects/",
        include(("projects.urls", "projects"), namespace="projects"),
    ),
    path(
        "accounts/",
        include(("accounts.urls", "accounts"), namespace="accounts"),
    ),
    path("api/", include("equestria.api.urls")),
]

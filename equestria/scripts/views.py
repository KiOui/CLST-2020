"""Module to handle uploading files."""
from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from os.path import basename, dirname
from django.views.static import serve
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied


class ProjectDeleteView(LoginRequiredMixin, TemplateView):
    """View for deleting projects."""

    template_name = "scripts/project-delete.html"

    def get(self, request, **kwargs):
        """
        GET request for ProjectDeleteView.

        :param request: the request
        :param kwargs: keyword arguments
        :return: a render of the project-delete page
        """
        project = kwargs.get("project")

        if not request.user.has_perm("access_project", project):
            raise PermissionDenied

        return render(request, self.template_name, {"project": project})

    def post(self, request, **kwargs):
        """
        POST request for ProjectDeleteView.

        Deletes a project and redirects to the project overview page
        :param request: the request
        :param kwargs: keyword arguments
        :return: a redirect to the project overview page
        """
        project = kwargs.get("project")
        project.delete()
        return redirect("projects:overview")


def download_project_archive(request, **kwargs):
    """
    Download all files of a project in ZIP format.

    :param request: the request
    :param kwargs: keyword arguments
    :return: a serve of a compressed archive of the project folder (ZIP format)
    """
    project = kwargs.get("project")

    zip_filename = project.create_downloadable_archive()
    return serve(request, basename(zip_filename), dirname(zip_filename))

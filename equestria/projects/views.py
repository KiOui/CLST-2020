from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from guardian.mixins import LoginRequiredMixin
from guardian.shortcuts import assign_perm
from pipelines.models import Pipeline
from projects.forms import ProjectCreateForm
from projects.models import Project, File
from .forms import UploadForm


class ProjectDetailView(LoginRequiredMixin, TemplateView):
    """View for initial upload of files to a project."""

    login_url = "/accounts/login/"

    template_name = "projects/project-detail.html"

    def get(self, request, **kwargs):
        """
        Handle a GET request for the file upload page.

        :param request: the request
        :param kwargs: keyword arguments
        :return: A render of the project detail page containing an upload form
        """
        project = kwargs.get("project")
        if not request.user.has_perm("access_project", project):
            raise PermissionDenied

        context = {"project": project}
        if project.can_upload():
            context["upload_form"] = UploadForm()
        return render(request, self.template_name, context)


class ProjectOverview(LoginRequiredMixin, TemplateView):
    """Class to handle get requests to the project overview page."""

    login_url = "/accounts/login/"

    template_name = "projects/project-overview.html"

    def get(self, request, **kwargs):
        """
        Handle requests to the project create page.

        Get requests are handled within this class while the upload
        post requests are handled in the upload app
        with callback URLs upload/wav and upload/txt.
        """
        pipelines = Pipeline.objects.all()
        form = ProjectCreateForm(request.user, None, pipelines=pipelines)
        projects = Project.objects.filter(user=request.user.id)
        return render(
            request, self.template_name, {"form": form, "projects": projects},
        )

    def post(self, request, **kwargs):
        """
        POST request for the project create page.

        :param request: the request
        :param kwargs: keyword arguments
        :return: a render of the fa-project-create page
        """
        pipelines = Pipeline.objects.all()
        form = ProjectCreateForm(
            request.user, request.POST, pipelines=pipelines
        )
        projects = Project.objects.filter(user=request.user.id)
        if form.is_valid():
            pipeline_id = form.cleaned_data.get("pipeline")
            project_name = form.cleaned_data.get("project_name")
            pipeline = Pipeline.objects.get(id=pipeline_id)
            project = Project.objects.create(
                name=project_name, pipeline=pipeline, user=request.user
            )
            assign_perm("access_project", request.user, project)
            return redirect("upload:upload_project", project=project)
        return render(
            request, self.template_name, {"form": form, "projects": projects},
        )

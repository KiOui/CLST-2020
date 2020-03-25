from django.conf import settings
import os
import secrets
from django.http import Http404
from django.shortcuts import render
from django.views.generic import TemplateView
from django.shortcuts import redirect
from script_runner.models import Script, Profile, Process, InputTemplate
from script_runner.clamhelper import start_project, start_clam_server

# Create your views here.


class FAView(TemplateView):
    """Class to handle get requests to the forced alignment page."""

    """Forced allignment view."""

    template_name = "fa-project-create.html"

    def get(self, request, **kwargs):
        """
        Handle requests to the /forced page.

        Get requests are handled within this class while the upload
        post requests are handled in the upload app
        with callback URLs upload/wav and upload/txt.
        """
        if not request.user.is_authenticated:
            return redirect("%s?next=%s" % (settings.LOGIN_URL, request.path))
        else:
            fa_scripts = Script.objects.filter(forced_alignment_script=True)
            return render(
                request, self.template_name, {"fa_scripts": fa_scripts}
            )

    def post(self, request, **kwargs):
        """
        POST request for the fa-project-create page.

        :param request: the request
        :param kwargs: keyword arguments
        :return: a render of the fa-project-create page
        """
        project_name = request.POST.get("project-name", None)
        script_id = request.POST.get("script-id", None)
        fa_script = Script.objects.filter(forced_alignment_script=True).get(
            id=script_id
        )
        if project_name is None or fa_script is None:
            return render(request, self.template_name, {"failed": True})
        else:
            process = start_project(project_name, fa_script)
            return redirect("forcedAlign:fa_project", project=process.id)


class ForcedAlignmentProjectDetails(TemplateView):
    """Project overview page."""

    template_name = "fa-project-details.html"

    def get(self, request, **kwargs):
        """
        GET request for project overview page.

        :param request: the request
        :param kwargs: keyword arguments
        :return: A render of 404 or fa-project-details page
        """
        process = Process.objects.get(id=kwargs.get("project"))
        if process is not None:
            profiles = Profile.objects.filter(process=process)
            for profile in profiles:
                profile.input_templates = InputTemplate.objects.select_related().filter(
                    corresponding_profile=profile.id
                )
            return render(
                request,
                self.template_name,
                {"profiles": profiles, "process": process},
            )
        else:
            raise Http404("Project not found")

    def post(self, request, **kwargs):
        """
        POST request for project overview page.

        :param request: the request
        :param kwargs: keyword arguments
        :return: A 404 or redirecto to the fa_project page
        """
        profile_id = request.POST.get("profile_id", None)
        if profile_id is None:
            raise Http404("Bad request")

        profile = Profile.objects.get(pk=profile_id)

        if self.run_profile(profile, request.FILES):
            return redirect(
                "forcedAlign:fa_project", project=profile.process.id
            )
        else:
            raise Http404("Something went wrong with processing the files.")

    def run_profile(self, profile, files):
        """
        Run a specified process with the given profile.

        :param profile_id: the profile id to run
        :param files: the files to be uploaded to the CLAM server
        :return: None
        """
        argument_files = list()
        for input_template in InputTemplate.objects.select_related().filter(
            corresponding_profile=profile
        ):
            random_token = secrets.token_hex(32)
            file_name = os.path.join(settings.TMP_DIR, random_token)
            with open(file_name, "wb",) as file:
                for chunk in files[str(input_template.id)]:
                    file.write(chunk)
            argument_files.append((file_name, input_template.template_id,))
        start_clam_server(profile, argument_files)
        return True

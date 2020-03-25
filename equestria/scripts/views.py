from django.http import HttpResponseNotFound, Http404
from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from os.path import basename, dirname
from django.views.static import serve
from .models import Process, Profile, InputTemplate, Script
from django.http import JsonResponse
from scripts.clamhelper import start_clam_server, update_script, start_project
from django.conf import settings
import secrets
import os


class JsonProcess(TemplateView):
    """View for representing Processes as JSON."""

    def get(self, request, **kwargs):
        """
        Get request, actually redirecting everything to the POST method.

        :param request: the request of the user
        :param kwargs: the keyword arguments
        :return: the same as self.post returns
        """
        return self.post(request, **kwargs)

    def post(self, request, **kwargs):
        """
        Post request, used for serving AJAX requests the information they need.

        :param request: the request of the user
        :param kwargs: the keyword arguments
        :return: a JsonResponse containing the following information:
                    - status (of the process)
                    - status_message
                    - errors (true or false, if errors occurred)
                    - error_message (emtpy if no errors occurred, a message otherwise)
        """
        key = kwargs.get("process")
        process = Process.objects.get(pk=key)
        clam_info = update_script(process)
        if clam_info is None:
            return JsonResponse({"django_status": process.status,})
        else:
            return JsonResponse(
                {
                    "clam_status": clam_info.status,
                    "status_message": clam_info.statusmessage,
                    "django_status": process.status,
                    "errors": clam_info.errors,
                    "error_message": clam_info.errormsg,
                }
            )


class FAView(TemplateView):
    """Class to handle get requests to the forced alignment page."""

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
        project_name = request.POST.get("project-name", None)
        script_id = request.POST.get("script-id", None)
        fa_script = Script.objects.filter(forced_alignment_script=True).get(
            id=script_id
        )
        if project_name is None or fa_script is None:
            return render(request, self.template_name, {"failed": True})
        else:
            process = start_project(project_name, fa_script)
            return redirect("scripts:fa_project", process=process.id)


class ForcedAlignmentProjectDetails(TemplateView):

    template_name = "fa-project-details.html"

    def get(self, request, **kwargs):
        """
        GET request for the forced alignment project details page.

        :param request: the request
        :param kwargs: the keyword arguments
        :return: a 404 if the project is not found, a fa-project-details page otherwise
        """
        process = Process.objects.get(id=kwargs.get("process"))
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
        profile_id = request.POST.get("profile_id", None)
        if profile_id is None:
            raise Http404("Bad request")

        profile = Profile.objects.get(pk=profile_id)

        if ForcedAlignmentProjectDetails.run_profile(profile, request.FILES):
            return redirect(
                "scripts:fa_project", process=profile.process.id
            )
        else:
            raise Http404("Something went wrong with processing the files.")

    @staticmethod
    def run_profile(profile, files):
        """
        Run a specified process with the given profile.

        :param profile: the profile to run
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


def download_process_archive(request, **kwargs):
    """Download the archive containing the process files."""
    process = Process.objects.get(pk=kwargs.get("process"))
    if process.output_file is not None:
        return serve(
            request, basename(process.output_file), dirname(process.output_file)
        )
    else:
        return HttpResponseNotFound("Downloaded archive not found")

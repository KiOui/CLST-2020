"""Module to handle uploading files."""
import os
from django.http import Http404
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from .forms import UploadForm
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.mixins import LoginRequiredMixin
import zipfile
from django.core.exceptions import PermissionDenied


class UploadProjectView(LoginRequiredMixin, TemplateView):
    """View for initial upload of files to a project."""

    login_url = "/accounts/login/"

    template_name = "upload/upload-project.html"

    def get(self, request, **kwargs):
        """
        Handle a GET request for the file upload page.

        :param request: the request
        :param kwargs: keyword arguments
        :return: A render of the upload_project.html page containing an upload form if files can be uploaded to the
        project and a profile form if a new process can be started for the project
        """
        project = kwargs.get("project")
        if not request.user.has_perm("access_project", project):
            raise PermissionDenied
        files = os.listdir(project.folder)
        no_wav_list = []
        no_txt_list = []
        for file in files:
            if file.endswith(".txt") or file.endswith(".tg"):
                wavname = os.path.splitext(file)[0] + ".wav"
                if wavname not in files:
                    no_wav_list.append(file)
            if file.endswith(".wav"):
                txtname = os.path.splitext(file)[0] + ".txt"
                tgname = os.path.splitext(file)[0] + ".tg"
                if txtname not in files and tgname not in files:
                    no_txt_list.append(file)
        context = {
            "project": project,
            "files": files,
            "no_wav_list": no_wav_list,
            "no_txt_list": no_txt_list,
        }
        if project.can_upload():
            context["upload_form"] = UploadForm()
        if project.can_start_new_process():
            context["can_start"] = True
        return render(request, self.template_name, context)

    def post(self, request, **kwargs):
        """
        Handle POST request for file upload page.

        :param request: the request
        :param kwargs: keyword arguments
        :return: a ValueError if the profile in the form is not valid, a render of the upload_project.html page if there
        is already a started process, a redirect to the fa_start view otherwise
        """
        project = kwargs.get("project")
        if not project.can_start_new_process():
            return self.get(request, **kwargs)
        return redirect(
            "scripts:start_automatic",
            project=project,
            script=project.pipeline.fa_script,
        )


def upload_file_view(request, **kwargs):
    """
    Upload file view for uploading a file from a form.

    :param request: the request
    :param kwargs: keyword arguments
    :return: a redirect if the file upload succeeded, raises a StateException if the file can't be uploaded because the
    project has a running process
    """
    project = kwargs.get("project")
    if not project.can_upload():
        raise Http404("Can't upload files to this project")
    upload_form = UploadForm(request.POST, request.FILES)
    if upload_form.is_valid():
        uploaded_files = request.FILES.getlist("f")
        for file in uploaded_files:
            check_file_extension(project, file)
    return redirect("upload:upload_project", project=project)


def check_file_extension(project, file):
    """
    Check the file extension of the given file.

    :param project: the project to save the file to
    :param file: the file to be checked
    :return: None
    """
    ext = file.name.split(".")[-1]
    if ext == "zip":
        save_zipped_files(project, file)
    elif ext in ["wav", "txt", "tg"]:
        save_file(project, file)
    else:
        print("Filetype not allowed")


def save_zipped_files(project, file):
    """
    Save zipped files to a project.

    :param project: the project to save the file to
    :param file: the zip file of type <class 'django.core.files.uploadedfile.InMemoryUploadedFile'>
    :return: None
    """
    with zipfile.ZipFile(file) as zip_file:
        names = zip_file.namelist()
        for name in names:
            with zip_file.open(name) as file:
                check_file_extension(project, file)


def save_file(project, file):
    """
    Save a file to a project.

    :param project: the project to save the file to
    :param file: the file to be uploaded
    :return: None
    """
    path = project.folder
    fs = FileSystemStorage(location=path)
    if fs.exists(file.name):
        """Delete previously uploaded file with same name."""
        fs.delete(file.name)

    fs.save(file.name, file)

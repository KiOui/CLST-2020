import os
import shutil
from pathlib import Path

from scripts.models import Process, Profile
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from pipelines.models import Pipeline
from scripts.services import zip_dir
from .services import remove_files_from_directory

User = get_user_model()


def project_folder_path(instance, filename):
    """Get a project folder path."""
    return os.path.join(instance.project.folder, filename)


class Project(models.Model):
    """Project model class."""

    UPLOADING = 0
    FA_RUNNING = 1
    G2P_RUNNING = 2
    CHECK_DICTIONARY = 3

    TYPES = (
        (UPLOADING, "Uploading"),
        (FA_RUNNING, "FA running"),
        (G2P_RUNNING, "G2P running"),
        (CHECK_DICTIONARY, "Check dictionary"),
    )

    EXTRACT_FOLDER = "extract"
    OUTPUT_FOLDER = "output"

    name = models.CharField(max_length=512)
    pipeline = models.ForeignKey(
        Pipeline, on_delete=models.CASCADE, blank=False, null=False
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=False, blank=False
    )

    @property
    def absolute_path(self):
        """Get the absolute path of the project folder."""
        return os.path.join(
            os.path.join(
                os.path.join(settings.MEDIA_ROOT, settings.USER_DATA_FOLDER),
                self.user.username,
            ),
            self.name,
        )

    @property
    def folder(self):
        """Get the relative path (relative to the media folder) of the project folder."""
        return os.path.join(
            os.path.join(settings.USER_DATA_FOLDER, self.user.username),
            self.name,
        )

    def save(self, *args, **kwargs):
        """Save project."""
        Path(self.absolute_path).mkdir(parents=True, exist_ok=True)
        return super().save(*args, **kwargs)

    def clear_project_folder(self):
        """Clear the project folder and remove all File objects associated to it."""
        File.objects.filter(project=self).delete()
        remove_files_from_directory(self.absolute_path)

    def move_extracted_files(self, extensions):
        """
        Move extracted files to the project folder.

        :param extensions: the allowed extensions
        :return: a list of non-moved files
        """
        non_copied = list()
        if os.path.exists(os.path.join(self.folder, Project.EXTRACT_FOLDER)):
            for root, _, files in os.walk(
                os.path.join(self.folder, Project.EXTRACT_FOLDER)
            ):
                for file in files:
                    name, extension = os.path.splitext(file)
                    if extension[1:] in extensions:
                        shutil.copy(os.path.join(root, file), self.folder)
                    else:
                        non_copied.append(file)
        return non_copied

    def __str__(self):
        """Convert this object to string."""
        return self.name

    @property
    def status(self):
        """
        GET the status of this project.

        :return: the next step of this project
        """
        return self.get_next_step()

    def get_next_step(self):
        """
        Get the project status.

        :return: a value in self.TYPES indicating the project status
        """
        return self.UPLOADING

    def write_oov_dict_file_contents(self, content, name="default.oov.dict"):
        """
        Write content to .oov.dict file in project folder.

        :param content: the content to write to the file
        :param name: the name of the default file to write to
        :return: None
        """
        path = self.get_oov_dict_file_path()
        if path is not None:
            with open(path, "w") as file:
                file.write(content)
        else:
            with open(os.path.join(self.folder, name), "w") as file:
                file.write(content)

    def get_oov_dict_file_contents(self):
        """
        Get the content of the .oov.dict file in the project folder.

        :return: the content of the .oov.dict file, an emtpy string if such a file does not exist
        """
        path = self.get_oov_dict_file_path()
        if path is not None:
            with open(path, "r") as file:
                return file.read()
        else:
            return ""

    def get_oov_dict_file_path(self):
        """
        Get the file path of the .oov.dict file in the folder directory.

        :return: the file path of the .oov.dict file, or None if such a file does not exist
        """
        for file_name in os.listdir(self.absolute_path):
            full_file_path = os.path.join(self.absolute_path, file_name)
            if os.path.isfile(full_file_path):
                if file_name.endswith(".oov.dict"):
                    return full_file_path
        return None

    def has_non_empty_extension_file(self, extensions, folder=None):
        """
        Check if a file ends with some extension.

        :param extensions: a list of extensions that are valid.
        :param folder: the folder to check, if None this function uses self.folder
        :return: True if an .extension file is present with some text, False otherwise. Note: we may have multiple
        files, but as long as one is non empty we return true. (e.g. we have a.ext and b.ext, a is empty but b is not
        thus we return true).
        """
        if folder is None:
            folder = self.absolute_path

        if not os.path.exists(folder) or not os.path.isdir(folder):
            return False
        if type(extensions) is not list:
            raise TypeError("Extensions must be a list type")
        for file_name in os.listdir(folder):
            full_file_path = os.path.join(folder, file_name)
            if os.path.isfile(full_file_path):
                if file_name.endswith(tuple(extensions)):
                    if os.stat(full_file_path).st_size != 0:
                        return True

        return False

    def finished_fa(self):
        """
        Check if FA has finished.

        :return: True if a .ctm file is present in the project directory, False otherwise
        """
        return self.has_non_empty_extension_file(
            ["ctm"], folder=os.path.join(self.folder, Project.OUTPUT_FOLDER),
        )

    def create_downloadable_archive(self):
        """
        Create a downloadable archive.

        :return: the filename of the downloadable archive
        """
        _, zip_filename = os.path.split(self.folder)
        zip_filename = zip_filename + ".zip"
        return os.path.join(
            self.folder,
            zip_dir(self.folder, os.path.join(self.folder, zip_filename)),
        )

    def can_upload(self):
        """
        Check whether files can be uploaded to this project.

        :return: True if files can be uploaded to this project, False otherwise
        """
        return True

    def can_start_new_process(self):
        """
        Check whether a new process can be started for this project.

        :return: True if there are not running processes for this project, False otherwise
        """
        return self.current_process is None

    def start_fa_script(self, profile, **kwargs):
        """
        Start the FA script with a given profile.

        :param profile: the profile to start FA with
        :return: the process with the started script, raises a ValueError if the files in the folder do not match the
        profile, raises an Exception if a CLAM error occurred
        """
        return self.start_script(profile, self.pipeline.fa_script, **kwargs)

    def start_g2p_script(self, profile, **kwargs):
        """
        Start the G2P script with a given profile.

        :param profile: the profile to start G2P with
        :return: the process with the started script, raises a ValueError if the files in the folder do not match the
        profile, raises an Exception if a CLAM error occurred
        """
        return self.start_script(profile, self.pipeline.g2p_script, **kwargs)

    def start_script(self, profile, script, parameter_values=None):
        """
        Start a new script and add the process to this project.

        :param parameter_values: parameter values in (key, value) format in a dictionary
        :param profile: the profile to start the script with
        :param script: the script to start
        :return: the process with the started script, raises a ValueError if the files in the folder do not match the
        profile, raises an Exception if a CLAM error occurred
        """
        parameter_values = (
            dict() if parameter_values is None else parameter_values
        )

        if not self.can_start_new_process():
            raise Project.StateException
        elif profile.script != script:
            raise Profile.IncorrectProfileException

        self.current_process = Process.objects.create(
            script=script, folder=self.folder
        )
        self.save()
        try:
            self.current_process.start_safe(
                profile, parameter_values=parameter_values
            )
            return self.current_process
        except Exception as e:
            self.cleanup()
            raise e

    def cleanup(self):
        """
        Reset the project to a clean state.

        Resets the current process to None
        :return: None
        """
        self.current_process = None
        self.save()

    def delete(self, **kwargs):
        """
        Delete a Project.

        :param kwargs: keyword arguments
        :return: None, deletes a project and removes the folder of that project
        """
        if os.path.exists(self.folder):
            shutil.rmtree(self.folder, ignore_errors=True)
        super(Project, self).delete(**kwargs)

    def is_project_script(self, script):
        """
        Check if a script corresponds to this project.

        :param script: the script to check
        :return: True if it corresponds to this project, False otherwise
        """
        return (
            script == self.pipeline.fa_script
            or script == self.pipeline.g2p_script
        )

    class StateException(Exception):
        """Exception to be thrown when the project has an incorrect state."""

        pass

    class Meta:
        """Meta class for Project model."""

        unique_together = ("name", "user")
        permissions = [
            ("access_project", "Access project"),
        ]


class File(models.Model):
    """File class for project."""

    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, blank=False, null=False
    )
    file = models.FileField(
        upload_to=project_folder_path, blank=False, null=False, unique=True
    )

    @property
    def filename(self):
        """Get the filename."""
        return os.path.basename(self.file.name)

    @property
    def absolute_file_path(self):
        """Get the absolute path to the file."""
        return os.path.join(self.project.absolute_path, self.file.name)

    @property
    def file_path(self):
        """Get the relative path (relative to the media folder) of the file."""
        return os.path.join(self.project.folder, self.file.name)

    def save(self, *args, **kwargs):
        """Save method."""
        # Remove the file object if it already exists
        if File.objects.filter(
            project=self.project, file=self.file_path
        ).exists():
            File.objects.get(project=self.project, file=self.file_path).delete()
        # Also remove the file such that the original filename is retained
        if os.path.exists(self.absolute_file_path):
            os.remove(self.absolute_file_path)
        return super().save(*args, **kwargs)

    def __str__(self):
        """Convert this object to string."""
        return self.filename

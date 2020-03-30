from django.db.models import *
import clam.common.client
import clam.common.data
import clam.common.status

# Create your models here.

STATUS_CREATED = 0
STATUS_RUNNING = 1
STATUS_DOWNLOAD = 2
STATUS_FINISHED = 3
STATUS_ERROR = -1


class Script(Model):
    """
    Database model for scripts.

    Attributes:
        name                          Name of the script. Used for identification only, can be anything.
        script_file                   The file to execute.
        command                       Alternatively if script_file is None, the command to execute.
        primary_output_file           The file containing output of the script that should be displayed to the user.
        output_file_or_directory      The folder containing all output files.
                                      May be a single file if no such folder exists.
        img                           The image to display in script selection screens.
        icon                          If image is None, letters or FontAwesome icon to display instead.
        description                   Documentation of the purpose of the script.
    """

    name = CharField(max_length=512, blank=False, null=False)

    hostname = URLField(blank=False, null=False)

    img = ImageField(
        upload_to="script_img",
        blank=True,
        help_text="Thumbnail to symbolize script",
    )
    # If no image is provided, the icon is used instead

    description = TextField(max_length=32768, blank=True)

    forced_alignment_script = BooleanField(default=True)

    username = CharField(max_length=200, blank=True)
    password = CharField(max_length=200, blank=True)

    def __str__(self):
        """Use name of script in admin display."""
        return self.name

    class Meta:
        """
        Display configuration for admin pane.

        Order admin list alphabetically by name.
        Display plural correctly.
        """

        ordering = ["name"]
        verbose_name_plural = "Scripts"

    def get_clam_server(self):
        if self.username != "" and self.password != "":
            return clam.common.client.CLAMClient(self.hostname, self.username, self.password, basicauth=True)
        else:
            return clam.common.client.CLAMClient(self.hostname)


class Process(Model):
    """
    Database model for processes in CLAM.

    Attributes:
        name                          Name of the process.
                                      Used for identification only, can be anything.
        clam_id                       Identification number given by CLAM.
        output_path                   Path to the primary output file (e.g. output/error.log)
    """

    name = CharField(max_length=512, blank=False)
    script = ForeignKey(Script, on_delete=SET_NULL, blank=False, null=True)
    clam_id = CharField(max_length=256, blank=True)
    output_path = CharField(max_length=512, default="output/error.log")
    status = IntegerField(default=STATUS_CREATED)
    # TODO: Change this to a field of our user's files
    output_file = CharField(max_length=512, default=None, null=True, blank=True)

    def __str__(self):
        """Use name of process in admin display."""
        return self.name

    def get_status(self):
        """
        Get the status of this project in string format.

        :return: a string format of self.status
        """
        if self.status == 0:
            return "Ready to start"
        elif self.status == 1:
            return "Running"
        elif self.status == 2:
            return "Downloading results from CLAM server"
        elif self.status == 3:
            return "Done"
        elif self.status == -1:
            return "An error occurred"
        else:
            return "Unknown"

    class Meta:
        """
        Display configuration for admin pane.

        Order admin list alphabetically by name.
        Display plural correctly.
        """

        ordering = ["name"]
        verbose_name_plural = "Processes"


class Profile(Model):
    """
    Database model for profiles.

    A profile is a set of InputTemplates (possibly more later on)
    Attributes:
        process                 The process associated with this profile.
    """

    process = ForeignKey(Process, on_delete=SET_NULL, null=True)

    class Meta:
        """
        Display configuration for admin pane.

        Order admin list by id.
        Display plural correctly.
        """

        ordering = ["id"]
        verbose_name = "Profile"
        verbose_name_plural = "Profiles"

    def __str__(self):
        """
        Use identifier in admin pane.

        :return: string including the identifier of this object
        """
        return str(self.id)


class InputTemplate(Model):
    """
    Database model for input templates provided by the CLAM server.

    An input template is provided by CLAM and puts restrictions on what types of input files can be uploaded
    Attributes:
        template_id             The identifier of this input template in the CLAM server.
        format                  The format of this input template as a CLAM format.
        mime                    The accepted mime type
        label                   The label of this input template.
        extension               The accepted extension by this input template.
        optional                Whether or not this template is optional before starting the associated script.
        unique                  Whether or not there is only one of these files per process. If this equals True a file
                                must first be deleted before overwriting it on the CLAM server.
        accept_archive          Whether or not this template accepts archive files.
        corresponding_profile   The corresponding profile of this input template.
    """

    template_id = CharField(max_length=1024)
    format = CharField(max_length=1024)
    label = CharField(max_length=1024)
    mime = CharField(max_length=1024, default="text/plain")
    extension = CharField(max_length=32)
    optional = BooleanField()
    unique = BooleanField()
    accept_archive = BooleanField()
    corresponding_profile = ForeignKey(Profile, on_delete=SET_NULL, null=True)

    class Meta:
        """
        Display configuration for admin pane.

        Order admin list by id.
        Display plural correctly.
        """

        ordering = ["id"]
        verbose_name = "Input template"
        verbose_name_plural = "Input templates"


class InputFile(Model):
    """
    Database model for files used as inputs of scripts.

    Attributes:
        name                          Name of the file. 
                                      Used for identification only, can be anything.
        input_file                    Input file on disk.
        description                   Documentation of the purpose/content of the file.
        associated_process            Process object the file belongs to.
    """

    name = CharField(max_length=512)
    input_file = FilePathField(path="uploads/")  # TODO change this
    description = TextField(max_length=32768)
    associated_process = ManyToManyField(Process, default=None)

    def __str__(self):
        """Use name of input file in admin display."""
        return self.name

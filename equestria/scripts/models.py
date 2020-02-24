from django.db import models
from django.conf import settings
<<<<<<< HEAD
from .cron import JSONFile, JSONProcess, ProcessList, PROC_STARTING, PROC_RUNNING, PROC_FINISHED
from django.urls import reverse

# TODO: Set this in settings.py
DATABASE_FILE = "database.txt"


class Process(models.Model):
    process_id = models.AutoField(primary_key=True)
    input_file = models.FilePathField(path=settings.FILE_PATH_FIELD_DIRECTORY, default="")
    output_file = models.FilePathField(path=settings.FILE_PATH_FIELD_DIRECTORY, default="")
    status = models.CharField(max_length=10, default=PROC_STARTING)

    # TODO: Change this to return the actual script command
    def create_script_command(self):
        return "ls"

    def export_for_execution(self):
        if self.status == PROC_RUNNING:
            raise ValueError("This process is already running")

        database_file = JSONFile(DATABASE_FILE)
        process_list = ProcessList(database_file.get_json_content())
        process_to_add = JSONProcess(self.process_id, None, self.create_script_command(), PROC_STARTING)

        process_list.add_process(process_to_add)

        database_file.write(process_list.processes_to_dictionary())
        database_file.close()

        if self.status == PROC_FINISHED:
            self.set_starting()

    def set_finished(self):
        self.status = PROC_FINISHED

    def set_starting(self):
        self.status = PROC_STARTING

    def set_running(self):
        self.status = PROC_RUNNING

    def get_absolute_url(self):
        return reverse("scripts:script-detail", kwargs={"id": self.process_id})
=======
import subprocess
import os
import threading


def spawn_wait_thread():
    process = subprocess.Popen(['python3', os.path.join(settings.BASE_DIR, 'scripts/scriptje.py'), 'manage.py', 'bla'])
    Process.objects.create(process_id=process.pid, executing=True)
    print(process)
    process.communicate()
    notify_process_done(process)


def notify_process_done(process):
    print("Process is done!")


# TODO we may need to pass some POST arguments later on.
# (that is why this function looks so empty)
def execute_script():
    t1 = threading.Thread(target=spawn_wait_thread)
    t1.start()


class Process(models.Model):
    process_id = models.IntegerField(blank=False)
    input_file = models.FilePathField(path=settings.FILE_PATH_FIELD_DIRECTORY)
    output_file = models.FilePathField(path=settings.FILE_PATH_FIELD_DIRECTORY)
    executing = models.BooleanField(default=False)
>>>>>>> parent of 193d483... Process write to JSON

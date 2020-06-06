from zipfile import BadZipFile

from django.contrib.auth import get_user_model
from django.test import TestCase, Client, RequestFactory
from django.urls import reverse
from scripts.models import Project, Pipeline
from upload.views import *

from unittest.mock import patch
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.files.storage import FileSystemStorage
import base64

User = get_user_model()


class TestView(TestCase):
    """Check the view."""

    fixtures = ["uploadDB"]

    def setUp(self):
        """Set up the data needed to perform tests below."""
        self.project = Project.create_project(
            "test3", Pipeline.objects.get(id=1), User.objects.get(id=1)
        )

        self.url = reverse("upload:upload_project", args=[self.project])
        self.client = Client()

        # NOTE! this file must not be a zip file, or else other tests may fail.
        self.existing_file = SimpleUploadedFile(
            "existingFile.wav", b"file_content", content_type="wav"
        )
        self.invalid_file = SimpleUploadedFile(
            "invalid.xml", b"file_content", content_type="xml"
        )

    def tearDown(self):
        self.project.delete()

    @patch("os.listdir", return_value=["test.wav"])
    def test_get(self, mock):
        """Test a get request as admin."""
        self.client.login(username="admin", password="admin")

        data = {"f": self.existing_file}
        response = self.client.get(self.url, data)
        self.assertEqual(response.status_code, 200)
        print(mock.call_count)  # just for CI deadcode failing here

    @patch("os.listdir", return_value=["test.wav"])
    def test_get2(self, listdirMock):
        """Test a GET request with single wav file."""

        self.client.login(username="admin", password="admin")

        data = {"f": self.existing_file}
        response = self.client.get(self.url, data)
        self.assertEqual(response.status_code, 200)
        print(listdirMock.call_count)  # just for CI deadcode failing here

    @patch("os.listdir", return_value=["test.wav"])
    def test_POST1(self, mock):
        """Test whether uploading valid files works properly."""

        self.client.login(username="admin", password="admin")

        data = {"f": self.existing_file}
        response = self.client.post(self.url, data, format="multipart")
        self.assertEqual(response.status_code, 200)
        print(mock.call_count)  # just for CI deadcode failing here

    @patch("os.listdir", return_value=["test.wav"])
    @patch("scripts.models.Project.can_start_new_process", return_value=False)
    def test_POST2(self, can_start_new_mock, mock):
        """Test whether uploading valid files works properly and starts new process."""
        self.client.login(username="admin", password="admin")
        data = {"f": self.existing_file}
        response = self.client.post(self.url, data, format="multipart")
        self.assertEqual(response.status_code, 200)
        print(can_start_new_mock.call_count)  # Just for Ci deadcode analysis.
        print(mock.call_count)  # just for CI deadcode failing here

    def test_invalid_file_ext_upload(self):
        """Test whether uploading valid files fails properly."""
        self.client.login(username="admin", password="admin")

        data = {"f": self.invalid_file}

        response = self.client.post(self.url, data, format="multipart")
        self.assertEqual(response.status_code, 200)
        # TODO: once implemented, we should check if the user gets a
        # warning that an invalid file is uploaded.

    def test_save_zipped_files_fail(self):
        """Test if saving zipped files fails if uploading non zip file."""
        try:
            save_zipped_files(self.project, self.existing_file)
            self.fail(
                "uploading a non zip file to save_zipped_files should fail..."
            )
        except BadZipFile:
            assert True

    @patch("upload.views.save_file")
    def test_save_zipped_files(self, cfemock):
        """Test if zip file upload works."""
        file = SimpleUploadedFile(
            "coolzip.zip",
            base64.b64decode(
                "UEsDBBQACAAIALldmlAAAAAAAAAAABQAAAALACAAcGF5bG9hZC50eHRVVA0AB9/WpV4K16Ve39al\
XnV4CwABBOgDAAAE6AMAAFNITc7IV1DySM3JyVcIzy/KSVHiAgBQSwcIaHG+khYAAAAUAAAAUEsD\
BBQACAAIAMtdmlAAAAAAAAAAAA0AAAALACAAcGF5bG9hZC53YXZVVA0AB/7WpV4K16Ve/talXnV4\
CwABBOgDAAAE6AMAAEtNzshXUMowMspU4uICAFBLBwhuOur9DwAAAA0AAABQSwECFAMUAAgACAC5\
XZpQaHG+khYAAAAUAAAACwAgAAAAAAAAAAAApIEAAAAAcGF5bG9hZC50eHRVVA0AB9/WpV4K16Ve\
39alXnV4CwABBOgDAAAE6AMAAFBLAQIUAxQACAAIAMtdmlBuOur9DwAAAA0AAAALACAAAAAAAAAA\
AACkgW8AAABwYXlsb2FkLndhdlVUDQAH/talXgrXpV7+1qVedXgLAAEE6AMAAAToAwAAUEsFBgAA\
AAACAAIAsgAAANcAAAAAAA=="
            ),
            content_type="zip",
        )
        save_zipped_files(self.project, file)
        assert os.listdir(self.project.folder) == [
            "output"
        ]  # The number of files in our mocking return value.

    @patch("django.core.files.storage.FileSystemStorage.save")
    @patch("django.core.files.storage.FileSystemStorage.delete")
    def test_save_file_new(self, fsDeleteMock, fsSaveMock):
        """Test if saving a new file works."""

        self.client.login(username="admin", password="admin")
        file = SimpleUploadedFile(
            "newFile.wav", b"file_content", content_type="video/mp4"
        )
        path = self.project.folder
        fs = FileSystemStorage(location=path)
        assert not fs.exists(file.name)
        save_file(self.project, file)
        assert fsDeleteMock.call_count == 0
        assert fsSaveMock.call_count == 1

    @patch(
        "django.core.files.storage.FileSystemStorage.exists", return_value=True
    )
    @patch("django.core.files.storage.FileSystemStorage.save")
    @patch("django.core.files.storage.FileSystemStorage.delete")
    def test_save_file_existing(self, fsDeleteMock, fsSaveMock, fsExistsMock):
        """Test if saving existing files work."""

        self.client.login(username="admin", password="admin")
        save_file(self.project, self.existing_file)
        assert fsDeleteMock.call_count == 1
        assert fsSaveMock.call_count == 1
        assert fsExistsMock.call_count == 1

    @patch("scripts.models.Project.can_upload", return_value=False)
    def test_upload_file_view(self, canuploadMock):
        self.client.login(username="admin", password="admin")

        data = {"f": self.existing_file}
        request = RequestFactory().post(self.url, data, format="multipart")
        request.user = User.objects.get(id=1)
        try:
            view = UploadProjectView()
            view.post(request, project=self.project)
            self.fail("Should not be allowed to upload! should get 404")
        except Http404:
            pass

    @patch("scripts.models.Project.can_upload", return_value=True)
    def test_upload_file_view_true(self, canuploadMock):
        self.client.login(username="admin", password="admin")

        data = {"f": self.existing_file}
        request = RequestFactory().post(self.url, data, format="multipart")
        request.user = User.objects.get(id=1)
        view = UploadProjectView()
        view.post(request, project=self.project)
        assert True

    @patch("upload.views.save_file")
    def test_save_zipped_files_recurse(self, cfemock):
        """Test if zip file upload works."""
        file = SimpleUploadedFile(
            "coolzip.zip",
            base64.b64decode(
                "UEsDBBQACAAIAKUqu1AAAAAAAAAAALwAAAAIACAAZmlsZS56aXBVVA0ABzdbzl44W85eN1vOXnV4\
CwABBOgDAAAE6AMAAAvwZmYRYeAAwoVauwMYkAALgwJDWmZOamgILwO7XvS5OCMgBtGlFdwMjCwv\
mIFKQAQzQ4A3OwdIBxNUZ4A3I5MIM6qpTEimwsCSRhBJjB0B3qxsILWMQBgEpEPA+gFQSwcIGRa1\
qV4AAAC8AAAAUEsBAhQDFAAIAAgApSq7UBkWtaleAAAAvAAAAAgAIAAAAAAAAAAAAKSBAAAAAGZp\
bGUuemlwVVQNAAc3W85eOFvOXjdbzl51eAsAAQToAwAABOgDAABQSwUGAAAAAAEAAQBWAAAAtAAA\
AAAA"
            ),
            content_type="zip",
        )
        save_zipped_files(self.project, file)
        assert os.listdir(self.project.folder) == [
            "output"
        ]  # The number of files in our mocking return value.

    @patch("os.path.join", return_value="")
    @patch("os.remove")
    def test_Delete_file_view_non_exist(self, oremoveMock, pathjoinMock):
        self.client.login(username="admin", password="admin")

        data = {"file": self.existing_file}
        request = RequestFactory().post(self.url, data)
        try:
            delete_file_view(request, project=self.project)
            self.fail("file should not exist")
        except:
            pass

    @patch("os.path.exists", return_value=True)
    @patch("os.path.join", return_value="")
    @patch("os.remove")
    def test_Delete_file_view_exist(self, oremoveMock, joinMock, existMock):
        self.client.login(username="admin", password="admin")

        data = {"file": self.existing_file}
        request = RequestFactory().post(self.url, data)

        delete_file_view(request, project=self.project)

    @patch("shutil.rmtree")
    @patch("os.listdir", return_value=["dir1"])
    @patch("os.walk", return_value=["file1", "file2"])
    def test_handle_folders_no_file(self, walkMock, listdirMock, shutilRTMock):
        handle_folders(self.project)
        assert walkMock.call_count == 1
        assert listdirMock.call_count == 1
        assert shutilRTMock.call_count == 1

    @patch("os.remove")
    @patch("shutil.move")
    @patch("os.path.isfile", return_value=True)
    @patch("shutil.rmtree")
    @patch("os.listdir", return_value=["dir1"])
    @patch("os.walk", return_value=["file1", "file2"])
    def test_handle_folders(
        self,
        walkMock,
        listdirMock,
        shutilRTMock,
        fileMock,
        shutilMoveMock,
        osremoveMock,
    ):
        handle_folders(self.project)
        assert walkMock.call_count == 1
        assert listdirMock.call_count == 1
        assert shutilRTMock.call_count == 1
        assert shutilMoveMock.call_count == 1
        assert osremoveMock.call_count == 1

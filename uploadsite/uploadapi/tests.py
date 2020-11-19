from django.test import TestCase

from .models import File
import uuid
import datetime
from django.test import Client
from django.urls import reverse

from django.test.utils import setup_test_environment, teardown_test_environment

FILENAME = 'name'
FILE_UUID = uuid.uuid4()
USER_UUID = uuid.uuid4()
ZIP_FILENAME = 'zipfilename'

class FileModelTests(TestCase):
    """
        Tests File model
    """
    def test_file_constructor(self):
        now = datetime.datetime.now().timestamp()
        file = File(file_uuid=FILE_UUID, name=FILENAME, created_at=now, uploaded_at=now, zipname=ZIP_FILENAME, user_uuid=USER_UUID)
        expectedResult = '{}-{}-{}-{}-{}-{}'.format(FILE_UUID, FILENAME, now, now, ZIP_FILENAME, USER_UUID)
        self.assertTrue(str(file) == expectedResult)


def sanitize_times(t):
    """
        Remove microseconds and set up time zone to a datetime pbject
    """
    return t.replace(microsecond=0).replace(tzinfo=datetime.timezone.utc)


def create_file(d, file_uuid, user_uuid):
    """
        Uploads a file into the DB
    """
    File.objects.create(
        file_uuid=file_uuid,
        name=FILENAME,
        created_at=d,
        uploaded_at=d,
        zipname=ZIP_FILENAME,
        user_uuid=user_uuid)


class FileViewTests(TestCase):
    """
        Tests File view
    """

    def setUp(self):
        self.client = Client()


    def test_get_home_succeds(self):
        response = self.client.get('/')
        self.assertIs(response.status_code, 200)


    def test_get_files_succeds(self):
        # GIVEN
        # a new file created on the db
        now = datetime.datetime.now()
        now_sanitized = sanitize_times(now)
        create_file(now, FILE_UUID, USER_UUID)

        # WHEN
        # get the list of files
        response = self.client.get('/files/')

        # THEN
        # 1 response is obtained and its content is the expected
        list_of_responses = list(eval(response.content.decode('utf-8')))
        self.assertEquals(response.status_code, 200)
        self.assertEquals(len(list_of_responses), 1)
        fileResponse = list_of_responses[0]
        fileCreationTime = datetime.datetime.fromisoformat(fileResponse.get('created_at').replace("Z", "+00:00"))
        fileUpdateTime = datetime.datetime.fromisoformat(fileResponse.get('uploaded_at').replace("Z", "+00:00"))

        # Validate responses
        self.assertEquals(fileResponse.get('file_uuid'), str(FILE_UUID))
        self.assertEquals(fileResponse.get('name'), FILENAME)
        self.assertEquals(sanitize_times(fileCreationTime), now_sanitized)
        self.assertEquals(sanitize_times(fileUpdateTime), now_sanitized)
        self.assertEquals(fileResponse.get('zipname'), ZIP_FILENAME)
        self.assertEquals(fileResponse.get('user_uuid'), str(USER_UUID))


    def test_get_files_filter_user_uuid_not_empty(self):
        # GIVEN
        # a new file created on the db
        now = datetime.datetime.now()
        create_file(now, FILE_UUID, USER_UUID)

        # WHEN
        # get the list of files
        response = self.client.get('/files/?useruuid={}'.format(USER_UUID))
        list_of_responses = list(eval(response.content.decode('utf-8')))

        # THEN
        # only 1 response is expected
        self.assertEquals(response.status_code, 200)
        self.assertEquals(len(list_of_responses), 1)


    def test_get_files_filter_user_uuid_empty(self):
        # GIVEN
        # a new file created on the db
        now = datetime.datetime.now()
        create_file(now, FILE_UUID, USER_UUID)

        # WHEN
        # get the list of files
        response = self.client.get('/files/?useruuid={}'.format(uuid.uuid4()))
        list_of_responses = list(eval(response.content.decode('utf-8')))

        # THEN
        # zero response is expected
        self.assertEquals(response.status_code, 200)
        self.assertEquals(len(list_of_responses), 0)

    def test_get_files_filter_zipname_not_empty(self):
        # GIVEN
        # a new file created on the db
        now = datetime.datetime.now()
        create_file(now, FILE_UUID, USER_UUID)

        # WHEN
        # get the list of files
        response = self.client.get('/files/?zipname={}'.format(ZIP_FILENAME))
        list_of_responses = list(eval(response.content.decode('utf-8')))

        # THEN
        # only 1 response is expected
        self.assertEquals(response.status_code, 200)
        self.assertEquals(len(list_of_responses), 1)


    def test_get_files_filter_zipname_empty(self):
        # GIVEN
        # a new file created on the db
        now = datetime.datetime.now()
        create_file(now, FILE_UUID, USER_UUID)

        # WHEN
        # get the list of files
        response = self.client.get('/files/?zipname={}'.format(uuid.uuid4()))
        list_of_responses = list(eval(response.content.decode('utf-8')))

        # THEN
        # zero response is expected
        self.assertEquals(response.status_code, 200)
        self.assertEquals(len(list_of_responses), 0)


    def test_get_files_filter_fuuid_not_empty(self):
        # GIVEN
        # a new file created on the db
        now = datetime.datetime.now()
        create_file(now, FILE_UUID, USER_UUID)

        # WHEN
        # get the list of files
        response = self.client.get('/files/?fuuid={}'.format(FILE_UUID))
        list_of_responses = list(eval(response.content.decode('utf-8')))

        # THEN
        # only 1 response is expected
        self.assertEquals(response.status_code, 200)
        self.assertEquals(len(list_of_responses), 1)


    def test_get_files_filter_fuuid_empty(self):
        # GIVEN
        # a new file created on the db
        now = datetime.datetime.now()
        create_file(now, FILE_UUID, USER_UUID)

        # WHEN
        # get the list of files
        response = self.client.get('/files/?fuuid={}'.format(uuid.uuid4()))
        list_of_responses = list(eval(response.content.decode('utf-8')))

        # THEN
        # zero response is expected
        self.assertEquals(response.status_code, 200)
        self.assertEquals(len(list_of_responses), 0)


    def test_get_files_succeds_right_number_of_responses(self):
        # GIVEN
        # 20 files are stored on the DB
        now = datetime.datetime.now()
        # set up: upload 20 files
        for _ in range(20):
            create_file(now, uuid.uuid4(), uuid.uuid4())

        # WHEN
        # get the list of files
        response = self.client.get('/files/')
        list_of_responses = list(eval(response.content.decode('utf-8')))

        # THEN
        # 20 files are retrieved
        self.assertEquals(response.status_code, 200)
        self.assertEquals(len(list_of_responses), 20)

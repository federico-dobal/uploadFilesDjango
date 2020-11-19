from django.http import HttpResponse, HttpResponseBadRequest
from django.core.exceptions import ValidationError
from django.shortcuts import render

from rest_framework import viewsets
from rest_framework.parsers import MultiPartParser, FileUploadParser

from .models import File
from .serializers import FileSerializer

import zipfile
import tempfile
import os
import uuid
import datetime

MIN_NUMBER_FILES, MAX_NUMBER_FILES = 1, 10


def insertFileRecords(file_paths, zip_filename, user_uuid):
    for filename in file_paths:
        File.objects.create(file_uuid=uuid.uuid4(),
            name=filename,
            created_at=datetime.datetime.now().timestamp(),
            uploaded_at=datetime.datetime.now().timestamp(),
            zipname=zip_filename,
            user_uuid=user_uuid)


class FileUploadView(viewsets.ModelViewSet):

    queryset = File.objects.all().order_by('uploaded_at')
    serializer_class = FileSerializer
    parser_classes = (MultiPartParser,)


    def _build_queryset(self):
        queryset = File.objects.all()

        # Search by zip user uuid
        user_uuid = self.request.GET.get('useruuid', None)
        if user_uuid is not None:
            queryset = queryset.filter(user_uuid=user_uuid)

        # Search by zip file name
        zip_filename = self.request.GET.get('zipname', None)
        if zip_filename is not None:
            queryset = queryset.filter(zipname=zip_filename)

        # Search by zip file name
        file_uuid = self.request.GET.get('fuuid', None)
        if file_uuid is not None:
            queryset = queryset.filter(file_uuid=file_uuid)
        return queryset


    def get_queryset(self):
        if self.request.method == 'GET':
            return self._build_queryset()


    def createZipFile(self, FILES):
        """
            Creates a zip file with the files provifed on the parameter.
            Return the files names included on the zip file and the zip file name

            Arguments:
                FILES: list of files to include in the zip file
        """
        zip_filename = '{}.zip'.format(uuid.uuid4())
        file_paths = []
        with zipfile.ZipFile(zip_filename, 'w') as myzip:

            for ix in range(1, 11):
                file_header = 'file_{}'.format(ix)
                if file_header in FILES.keys():
                    new_file, filename = tempfile.mkstemp()
                    # store file path to import if zip creation succeeds
                    file_paths.append(filename)

                    # write and close file
                    os.write(new_file, FILES.get(file_header).read())
                    os.close(new_file)

                    # write zipfile
                    myzip.write(filename)
        return file_paths, zip_filename


    def put(self, request, filename=None, format=None):

        # check whether client provides files
        if not request.FILES:
            return HttpResponseBadRequest('File(s) not provided')

        # At least 1 file should be provided and it accepts a maximum of MIN_NUMBER_FILES files
        if len(request.FILES) < MIN_NUMBER_FILES or len(request.FILES) > MAX_NUMBER_FILES:
            message = 'Incorect number of files provided. Min number is {} and maximum number of files is {}'.format(MIN_NUMBER_FILES, MAX_NUMBER_FILES)
            return HttpResponseBadRequest(message)

        user_uuid = request.data.get('user_uuid')
        # check whether client provides user uuid
        if not user_uuid:
            return HttpResponseBadRequest('User uuid not provided')

        try:
            # list of filenames to store into db
            file_names, zip_filename = self.createZipFile(request.FILES)

            # import filenames into DB
            insertFileRecords(file_names, zip_filename, user_uuid)

        except ValidationError:
            return HttpResponseServerError('Server failed to inser records')

        # if all is fine then return succesfully
        response =  HttpResponse(open(zip_filename, 'rb'),
            status=200,
            content_type='application/force-download')
        response['Content-Disposition'] = 'attachment; filename="%s"' % zip_filename
        return response

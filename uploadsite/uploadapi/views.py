from django.shortcuts import render

from rest_framework import viewsets
from rest_framework.parsers import MultiPartParser, FileUploadParser
from django.http import HttpResponse, HttpResponseBadRequest

from .models import File
from .serializers import FileSerializer

import zipfile
import tempfile
import os
import uuid
import datetime

ZIP_FILENAME = 'result_1.zip'
class FileUploadView(viewsets.ModelViewSet):
    queryset = File.objects.all().order_by('uploaded_at')
    serializer_class = FileSerializer
    parser_classes = (MultiPartParser,)

    def put(self, request, filename=None, format=None):

        # check whether client provides files
        if not request.FILES:
            return HttpResponseBadRequest('File(s) not provided')

        # At least 1 file should be provided and it accepts a maximum of 10 files
        if len(request.FILES) < 1 or len(request.FILES) > 10:
            return HttpResponseBadRequest('Incorect number of files provided. Min number is 1 and maximum number of files is 10')

        user_uuid = request.data.get('user_uuid')
        # check whether client provides user uuid
        if not user_uuid:
            return HttpResponseBadRequest('User uuid not provided')

        # list of filenames to store into db
        file_paths = []
        with zipfile.ZipFile(ZIP_FILENAME, 'w') as myzip:

            for ix in range(1, 11):
                file_header = 'file_{}'.format(ix)
                if file_header in request.FILES.keys():
                    new_file, filename = tempfile.mkstemp()
                    # store file path to import if zip creation succeeds
                    file_paths.append(filename)

                    # write and close file
                    os.write(new_file, request.FILES.get(file_header).read())
                    os.close(new_file)

                    # write zipfile
                    myzip.write(filename)

        # import filenames into DB
        for filename in file_paths:
            File.objects.create(file_uuid=uuid.uuid4(),
                name=filename,
                created_at=datetime.datetime.now().timestamp(),
                uploaded_at=datetime.datetime.now().timestamp(),
                zipname=ZIP_FILENAME,
                user_uuid=user_uuid)

        response =  HttpResponse(open(ZIP_FILENAME, 'rb'),
            status=204,
            content_type='application/force-download')
        response['Content-Disposition'] = 'attachment; filename="%s"' % ZIP_FILENAME
        return response

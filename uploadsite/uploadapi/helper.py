from .models import File

import uuid
import zipfile
import tempfile
import os
import datetime


def insertFileRecords(file_paths, zip_filename, user_uuid):
    """
        Inserts a file model into the DB
    """
    for filename in file_paths:
        File.objects.create(file_uuid=uuid.uuid4(),
            name=filename,
            created_at=datetime.datetime.now().timestamp(),
            uploaded_at=datetime.datetime.now().timestamp(),
            zipname=zip_filename,
            user_uuid=user_uuid)

def createZipFile(FILES):
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

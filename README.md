# uploadFilesDjango
Simple upload files API. It supports following functionality:

* Upload up to 10 files, zip them, store the metadata in DB and return the zipped content to the client.
* Query the uploaded files metadata:
** Retrieve all the uploaded files by user

# Environment setup

It requires to execute following commands:

        $ virtualenv venv_upload
        $ source venv_upload/bin/activate
        $ pip install -r requirements.txt

Also the developer might want to check environment dependencies:
        $ pip list

# Start the service

        $ cd uploadsite
        $ python manage.py makemigrations
        $ python manage.py migrate
        $ python manage.py runserver

# DB restore
DB can be rollbacked to the initial state, empty by executing following commands(TODO: automate it with an script):

        $ find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
        $ find . -path "*/migrations/*.pyc"  -delete
        $ rm db.sqlite3
        $ python manage.py makemigrations
        $ python manage.py migrate



# Queries of example:
## Get all the files(without pagination):

        $ curl --location --request GET 'http://127.0.0.1:8000/files?fuuid=ef5b85a4-f5d4-474c-b287-c825dd2f17f3'

## Get all the files filtered by user uuid:
  curl --location --request GET 'http://127.0.0.1:8000/files?useruuid=5138c2e3-a8ca-46ad-93f2-aee106acb97d'

## Get all the files filtered by file uuid:

        $ curl --location --request GET 'http://127.0.0.1:8000/files?fuuid=ef5b85a4-f5d4-474c-b287-c825dd2f17f3'   

## Get all the files filtered by zip file name:

        $ curl --location --request GET 'http://127.0.0.1:8000/files?zipname=c9692514-6113-4b43-9dfe-1b4851916a56.zip'     

## Post a set of Files and receive the zipped file:

       $ curl --location --request PUT 'http://127.0.0.1:8000/files/' \
       --form 'file_1=@/{PATH_TO_FILE}/f1.txt' \
       --form 'file_2=@/{PATH_TO_FILE}/f2.txt' \
       --form 'file_3=@/{PATH_TO_FILE}/f3.txt' \
       --form 'user_uuid=5138c2e3-a8ca-46ad-93f2-aee106acb97d'

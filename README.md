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

* cd uploadsite
* python manage.py makemigrations
* python manage.py migrate
* python manage.py runserver

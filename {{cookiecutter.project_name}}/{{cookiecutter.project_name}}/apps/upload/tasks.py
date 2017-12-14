import base64

from celery.task import task

from {{cookiecutter.project_name}}.apps.upload.upload_photo import PhotoUpload


@task()
def upload_in_background(file_base64, key):
    file = base64.b64decode(file_base64.encode('utf-8'))
    file_upload = PhotoUpload()
    file_upload.do_request_upload(file, key)

import uuid

import boto3
from django.conf import settings

from {{cookiecutter.project_name}}.apps.upload.types import PhotoDirectoryFactory


class PhotoUpload:
    def __init__(self):
        self.bucket_name = settings.AWS_STORAGE_BUCKET_NAME

    @staticmethod
    def __request_file_name__():
        file_name = '%s.jpg' % uuid.uuid4()
        filedir = '/tmp/%s.jpg' % file_name
        return {'file_name': file_name, 'file_dir': filedir}

    def __get_url__(self, key):
        return 'https://s3.amazonaws.com/{bucket}/{key}'.format(bucket=self.bucket_name, key=key)

    @staticmethod
    def __get_key__(img_type, file_name):
        return "{0}{1}".format(PhotoDirectoryFactory.factory(img_type).value, file_name)

    def __save_file__(self, file):
        file_name = self.__request_file_name__()
        with open(file_name['file_dir'], 'wb+') as temp_file:
            for chunk in file.chunks():
                temp_file.write(chunk)
        return file_name

    def do_upload(self, file, type):
        file_name = self.__save_file__(file)

        key = self.__get_key__(type, file_name['file_name'])
        s3 = boto3.resource('s3')
        s3.Bucket(self.bucket_name).upload_file(file_name['file_dir'], key)
        return self.__get_url__(key)

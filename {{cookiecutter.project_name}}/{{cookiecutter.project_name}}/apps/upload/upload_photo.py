"""
    Module for with receive the file and send it
    to AWS s3
"""
import uuid

import boto3
from django.conf import settings

from {{cookiecutter.project_name}}.apps.upload.types import PhotoDirectoryFactory


class PhotoUpload:
    """
    Class for upload file to S3
    """
    def __init__(self):
        self.bucket_name = settings.AWS_STORAGE_BUCKET_NAME

    @staticmethod
    def __request_file_name__():
        file_name = '%s.png' % uuid.uuid4()
        filedir = '/tmp/%s.png' % file_name
        return {'file_name': file_name, 'file_dir': filedir}

    def get_url(self, key):
        return 'https://s3.amazonaws.com/{bucket}/{key}'.format(bucket=self.bucket_name, key=key)

    @staticmethod
    def get_key(img_type, file_name):
        return "{0}{1}".format(PhotoDirectoryFactory.factory(img_type).value, file_name)

    def do_request_upload(self, file, key):
        s3 = boto3.client('s3')
        s3.put_object(Bucket=self.bucket_name, Key=key, Body=file)
        return self.get_url(key)

    def do_local_upload(self, file_dir, file_type):
        file_name = self.__request_file_name__()
        key = self.get_key(file_type, file_name['file_name'])
        s3 = boto3.resource('s3')
        s3.Bucket(self.bucket_name).upload_file(file_dir, key)
        return self.get_url(key)

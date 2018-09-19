"""
Photo upload API View
"""

import base64

from uuid import uuid4

from rest_framework import permissions
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView

from {{cookiecutter.project_name}}.apps.upload.tasks import upload_in_background
from {{cookiecutter.project_name}}.apps.upload.upload_photo import PhotoUpload


class PhotoUploadAPI(APIView):
    """
    View to receive the file
    """
    permission_classes = (permissions.AllowAny,)
    parser_classes = (FormParser, MultiPartParser)

    def post(self, request):
        """
        Receive the file and send it to AWS S3
        Args:
            request:

        Returns:
            {'url': 'the public url in s3'}
        """
        file_upload = PhotoUpload()

        key = file_upload.get_key(request.GET['type'],
                                  '{file_name}.png'.format(file_name=uuid4().__str__()))

        file = request.FILES['file']

        file_upload.do_request_upload(file, key)

        return Response(status=200, data={'url': file_upload.get_url(key)})

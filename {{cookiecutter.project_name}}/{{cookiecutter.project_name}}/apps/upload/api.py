"""
Photo upload API View
"""
from rest_framework import permissions
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView

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
        file = request.FILES['file']
        return Response(status=200, data={
            'url': file_upload.do_request_upload(file, request.GET['type'])
        })

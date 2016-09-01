from rest_framework import permissions
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView

from {{cookiecutter.app_name}}.apps.upload.upload_photo import PhotoUpload


class PhotoUploadAPI(APIView):

    permission_classes = (permissions.AllowAny, )
    parser_classes = (FormParser, MultiPartParser)

    def post(self, request, format=None):
        file_upload = PhotoUpload()
        file = request.FILES['file']
        return Response(status=200, data={'url': file_upload.do_upload(file, request.GET['type'])})

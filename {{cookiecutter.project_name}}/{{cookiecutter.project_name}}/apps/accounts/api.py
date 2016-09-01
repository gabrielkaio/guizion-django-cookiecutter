from rest_framework.decorators import list_route
from rest_framework.response import Response
from rest_framework import viewsets

from {{cookiecutter.app_name}}.apps.accounts.models import User
from {{cookiecutter.app_name}}.apps.accounts.serializer import UserSerializer, ChangePasswordSerializer
from {{cookiecutter.app_name}}.apps.utils.error_factory import ErrorFactory, ErrorType
from {{cookiecutter.app_name}}.permissions import IsCreationOrIsAuthenticated, NoPermissionNeeded


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsCreationOrIsAuthenticated]

    def list(self, request, *args, **kwargs):
        return Response(status=401)

    @list_route(methods=['GET'])
    def me(self, request):
        serializer = self.get_serializer(request.user, many=False)
        return Response(data=serializer.data, status=200)

    @list_route(methods=['PATCH'], serializer_class=ChangePasswordSerializer)
    def change_pass(self, request):
        last_password = request.data['last_password']
        new_password = request.data['new_password']
        confirm = request.data['confirm_password']

        if not request.user.check_password(last_password) or not new_password == confirm:
            return Response(status=401, data=ErrorFactory.generate(ErrorType.invalid_password))

        request.user.set_password(new_password)
        request.user.save()
        return Response(status=200, data={'status': 'OK'})

    @list_route(methods=('POST',), permission_classes=(NoPermissionNeeded,))
    def lost_password(self, request):
        try:
            email = request.data['email']
            User.objects.get(email=email)
            from {{cookiecutter.app_name}}.apps.utils.recovery_password_rest import password_reset
            return password_reset(request=request)
        except User.DoesNotExist:
            return Response(status=400, data=ErrorFactory.generate(ErrorType.email_not_found))

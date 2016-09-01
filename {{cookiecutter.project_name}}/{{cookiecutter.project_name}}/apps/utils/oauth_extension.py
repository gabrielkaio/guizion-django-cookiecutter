from datetime import timedelta

import boto3
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from oauth2_provider.models import RefreshToken, AccessToken
from oauth2_provider.oauth2_backends import OAuthLibCore
from oauth2_provider.oauth2_validators import OAuth2Validator
from oauth2_provider.settings import oauth2_settings

from django.conf import settings

from {{cookiecutter.app_name}}.apps.accounts.models import Devices
from {{cookiecutter.app_name}}.config.base import DEVICE_AGENT_HEADER, DEVICE_TOKEN_HEADER


class OAuthLibCoreExtension(OAuthLibCore):
    def create_token_response(self, request):

        if DEVICE_AGENT_HEADER in request.META:
            if request.META[DEVICE_AGENT_HEADER].upper() == Devices.WEB.upper():
                return super(OAuthLibCoreExtension, self).create_token_response(request)
            else:
                if DEVICE_TOKEN_HEADER in request.META:
                    return super(OAuthLibCoreExtension, self).create_token_response(request)

        uri, http_method, body, headers = self._extract_params(request)
        uri = headers.get("Location", None)
        message = _('You need to send a Device Token Header')
        return uri, {"Content-Type": "application/json"}, '{"error": "' + str(message) + '"}', 400


class OAuthLibExtension(OAuth2Validator):
    def save_bearer_token(self, token, request, *args, **kwargs):

        if request.refresh_token:
            try:
                RefreshToken.objects.get(token=request.refresh_token).revoke()
            except RefreshToken.DoesNotExist:
                assert ()  # TODO though being here would be very strange, at least log the error

        expires = timezone.now() + timedelta(seconds=oauth2_settings.ACCESS_TOKEN_EXPIRE_SECONDS)
        if request.grant_type == 'client_credentials':
            request.user = None

        access_token = AccessToken(
            user=request.user,
            scope=token['scope'],
            expires=expires,
            token=token['access_token'],
            application=request.client)
        access_token.save()

        if 'refresh_token' in token:
            refresh_token = RefreshToken(
                user=request.user,
                token=token['refresh_token'],
                application=request.client,
                access_token=access_token
            )
            refresh_token.save()

            if DEVICE_TOKEN_HEADER in request.headers:
                self.save_device(request=request, access_token=access_token, refresh_token=refresh_token)

        token['expires_in'] = oauth2_settings.ACCESS_TOKEN_EXPIRE_SECONDS

    def save_device(self, request, access_token, refresh_token):
        device = Devices.objects.filter(device_token=request.headers[DEVICE_TOKEN_HEADER]).first()
        if device is not None:
            to_delete = AccessToken.objects.get(pk=device.access_token.id)
            device.access_token = access_token
            device.refresh_token = refresh_token
            device.user = request.user
            device.language = request.headers['HTTP_ACCEPT_LANGUAGE']
            device.save()
            to_delete.delete()
        else:
            application_arn = self.get_application_arn(request)
            device = Devices(device_token=request.headers[DEVICE_TOKEN_HEADER],
                             user=request.user,
                             access_token=access_token,
                             refresh_token=refresh_token,
                             language=request.headers['HTTP_ACCEPT_LANGUAGE'])

            operational_system = device.ANDROID if application_arn == settings.ANDROID_ARN else device.iOS
            device.operational_system = operational_system
            awsclient = boto3.client('sns')

            response = awsclient.create_platform_endpoint(
               PlatformApplicationArn=application_arn,
               Token=device.device_token,
            )

            device.arn = response['EndpointArn']
            return device.save()

    def get_application_arn(self, request):
        if "ANDROID" in request.headers[DEVICE_AGENT_HEADER].upper():
            return settings.ANDROID_ARN
        else:
            if "SANDBOX" in request.headers[DEVICE_AGENT_HEADER].upper():
                return settings.IOS_SANDBOX_ARN
            else:
                return settings.IOS_ARN
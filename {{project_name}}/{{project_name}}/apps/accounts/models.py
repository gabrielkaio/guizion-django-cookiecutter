import uuid

from django.conf import settings
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models

from model_utils import Choices
from model_utils.fields import StatusField

from oauth2_provider.models import AccessToken, RefreshToken

from {{app_name}}.apps.accounts.managers import UserManager


class User(AbstractBaseUser, PermissionsMixin, models.Model):
    class Meta:
        swappable = 'AUTH_USER_MODEL'
        verbose_name = 'user'
        verbose_name_plural = 'users'
        abstract = False

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True, null=False, blank=False)
    first_name = models.CharField('first name', max_length=30, blank=True, null=True)
    last_name = models.CharField('last name', max_length=30, blank=True, null=True)
    date_joined = models.DateTimeField('date joined', auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    is_staff = models.BooleanField(
        'staff_status',
        default=False,
        help_text='Designates whether the user can log into this admin site.',
    )

    is_active = models.BooleanField(
        'active',
        default=True,
        help_text=
        'Unselect this instead of deleting accounts.',
    )

    objects = UserManager()
    USERNAME_FIELD = 'email'

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = '{first_name} {last_name}'.format(first_name=self.first_name,
                                                      last_name=self.last_name)
        return full_name.strip()

    def get_short_name(self):
        "Returns the short name for the user."
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        """
        Sends an email to this User.
        """
        from django.core.mail import send_mail
        send_mail(subject, message, from_email, [self.email], **kwargs)


class DeviceMixin(object):
    OPERATIONAL_SYSTEM = Choices('iOS', 'iOS_SANDBOX', 'Android', 'Web')


class Devices(models.Model, DeviceMixin):
    ANDROID = 'Android'
    iOS = 'iOS'
    iOS_SANDBOX = 'iOS_SANDBOX'
    WEB = 'Web'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    arn = models.CharField(max_length=150, null=True, blank=True)
    device_token = models.CharField(max_length=250)
    operational_system = StatusField(choices_name='OPERATIONAL_SYSTEM', default='iOS', db_index=True)
    user = models.ForeignKey(User, related_name="devices")
    access_token = models.ForeignKey(AccessToken, related_name="access_token", null=True, blank=True)
    refresh_token = models.ForeignKey(RefreshToken, related_name="refresh_token", null=True, blank=True)
    language = models.CharField(max_length=7)

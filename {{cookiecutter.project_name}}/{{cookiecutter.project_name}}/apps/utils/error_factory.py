from enum import Enum

from django.utils.translation import gettext_lazy as _


class ErrorType(Enum):
    invalid_password = ('invalid_password', str(_('Invalid Password')))
    not_found = ('not_found', str(_('Not found')))
    email_not_found = ('email_not_found', str(_('E-mail not found')))


class ErrorFactory:

    @staticmethod
    def generate(type):
        return {'error': type.value[1],
                'type': type.value[0]}

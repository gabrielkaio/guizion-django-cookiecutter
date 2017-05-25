"""
    Module with Rest error factory
"""
from enum import Enum

from django.utils.translation import gettext_lazy as _


class ErrorType(Enum):
    invalid_password = ('invalid_password', str(_('Invalid Password')))
    not_found = ('not_found', str(_('Not found')))
    email_not_found = ('email_not_found', str(_('E-mail not found')))
    invalid_request = ('invalid_request', str(_('Invalid request')))
    course_not_found = ('course_not_found', str(_('Course not found')))
    invalid_discount_code = ('invalid_discount_code', str(_('Invalid discount code')))


class ErrorFactory:

    @staticmethod
    def generate(error_type):
        return {'error': error_type.value[1],
                'type': error_type.value[0]}

import warnings

from django.contrib.auth import get_user_model
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.tokens import default_token_generator
from django.utils.translation import gettext_lazy as _
from rest_framework.response import Response


class CustomResetPasswordForm(PasswordResetForm):
    def get_users(self, email):
        return get_user_model()._default_manager.filter(
            email__iexact=email, is_active=True)


def password_reset(request, is_admin_site=False,
                   email_template_name='registration/password_reset_email.html',
                   subject_template_name='registration/password_reset_subject.txt',
                   password_reset_form=CustomResetPasswordForm,
                   token_generator=default_token_generator,
                   from_email=None,
                   extra_context=None,
                   html_email_template_name='registration/password_reset_email.html',
                   extra_email_context=None):
    if request.method == "POST":
        form = password_reset_form(request.data)
        if form.is_valid():
            opts = {
                'use_https': request.is_secure(),
                'token_generator': token_generator,
                'from_email': from_email,
                'email_template_name': email_template_name,
                'subject_template_name': subject_template_name,
                'request': request,
                'html_email_template_name': html_email_template_name,
                'extra_email_context': extra_email_context,
            }
            if is_admin_site:
                opts = dict(opts, domain_override=request.get_host())
            form.save(**opts)
            return Response(status=200, data={'status': 'OK'})
    else:
        form = password_reset_form()
    context = {
        'form': form,
        'title': _('Password reset'),
    }
    if extra_context is not None:
        context.update(extra_context)
    return Response(status=200, data={'status': 'OK'})

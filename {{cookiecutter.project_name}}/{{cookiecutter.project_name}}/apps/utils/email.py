"""
Utils to send email's
"""

from django.core.mail import send_mail


def send_templated_mail(email, subject, html_template, params=None):
    from django.conf import settings
    from django.template.loader import render_to_string
    msg_plain = render_to_string(html_template, params)
    msg_html = render_to_string(html_template, params)
    send_mail(subject, msg_plain, from_email=settings.DEFAULT_FROM_EMAIL,
              recipient_list=[email], html_message=msg_html)

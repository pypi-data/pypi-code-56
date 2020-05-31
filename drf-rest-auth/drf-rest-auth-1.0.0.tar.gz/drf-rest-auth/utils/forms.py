"""
# Copyright © Nico Huebschmann
# Licensed under the terms of the MIT License
"""

from django.contrib.auth.forms import PasswordResetForm as DjangoPasswordResetForm
from django.core.mail import EmailMultiAlternatives


class PasswordResetForm(DjangoPasswordResetForm):
    def send_mail(self, subject_template_name, email_template_name,
                  context, from_email, to_email, html_email_template_name=None):

        subject = 'Password reset on ' + str(context.get('domain'))
        # Email subject *must not* contain newlines
        subject = ''.join(subject.splitlines())

        body = 'You are receiving this email because you requested a password reset ' \
               'for your user account at ' + str(context.get('domain')) + '.' \
               ' Please go to the following page and choose a new password:\n\n' \
               + str(context.get('reset_confirm_url')) + '\n\n' \
               'The validation token is: ' + str(context.get('token')) + '\n' + \
               'Your username, in case you have forgotten: ' + str(context.get('user')) + '\n\n' \
               'Thanks for using our services!'

        email = EmailMultiAlternatives(subject, body, from_email, [to_email])
        email.send()

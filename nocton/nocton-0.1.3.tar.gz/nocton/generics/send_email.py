from django.core.mail import send_mail, EmailMessage
from django.template.loader import render_to_string
# from email.mime.image import MIMEImage
from django.conf import settings
from nocton.tools.console import print_f
from django.core.validators import validate_email, ValidationError

'''
Classe mais simplificada de envio de email
'''
class Email:
    def __init__(self, title=None, template_path=None, context={}):
        self.title = title
        self.template_path = template_path
        self.context = context

    # Envia o email
    def send(self, to):
        if isinstance(to, str):
            to = [to]

        try:
            EMAIL_HOST_USER = validate_email(settings.EMAIL_HOST_USER)

            html_message = render_to_string(self.template_path, self.context)
            email = EmailMessage(self.title, html_message, EMAIL_HOST_USER, to)
            
            email.content_subtype = "html"
            print_f('ENVIANDO EMAIL...')

            email.send()
        except ValidationError as error:
            print_f(f"Erro de validação de email: {error}")
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
import re


'''
    Validação de número de telefone para charfields em models
'''
def phone_validation(value):
    valid = re.compile('^\([1-9]{2}\)[ ]?(?:[2-8]|9[1-9])[0-9]{3}[ ]?\-[ ]?[0-9]{4}$')

    if not valid.match(value):
        raise ValidationError(
            _('Envie um número no formato "(XX) XXXX-XXXX" ou "(XX) 9XXXX-XXXX"'),
            params={'value': value},
        )
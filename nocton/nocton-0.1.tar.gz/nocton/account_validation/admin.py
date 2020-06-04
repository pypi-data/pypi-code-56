from django.contrib import admin
from nocton.account_validation.models import AccountValidatorToken

'''
Registra a banco de dados de validação de token
'''

admin.site.register(AccountValidatorToken)
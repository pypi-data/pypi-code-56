from django.conf import settings
from nocton.tools.console import print_f

# Carrega as informações do NOCTON
def load_nocton():
    try:
        NOCTON_SETTINGS = settings.NOCTON
    except AttributeError:
        # Caso não consiga, retorna um erro
        print("Erro")
        print_f("As configurações do NOCTON não foram definidas, talvez algumas coisas não funcionem como deveriam", destac=True, lenght=53)
            
        return False
    return NOCTON_SETTINGS

# Carrega uma informação qualquer das configurações do NOCTON, caso não consiga, retorna default
def load_setting(setting, default=None):
    try:
        return load_nocton().get(setting)
    except AttributeError as error:
        return default

# Carrega as informações de "watch"
def load_watch_settings(default=None):
    return load_setting('watch', default=default)

# Carrega as informações de validação
def load_account_validaton_settings(default=None):
    return load_setting('account_validation', default=default)
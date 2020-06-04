from nocton.setup.settings import load_account_validaton_settings
from nocton.tools.console import print_f


# Retorna as configurações de validação de conta
def get_account_validator_settings():
    account_validation_settings = load_account_validaton_settings({})

    if not isinstance(account_validation_settings, dict):
        account_validation_settings = {}

    return account_validation_settings

# Retorna se a validação de conta automática está ativada
def validation_enable():
    account_validation_settings = load_account_validaton_settings()
    

    if account_validation_settings == None:
        return False

    if isinstance(account_validation_settings, dict):
        if account_validation_settings.get('active_by_default') == False:
            return False

    return True

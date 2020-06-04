from django.utils.module_loading import import_string
from nocton.setup import load_account_validaton_settings
from nocton.tools import print_f

class BasicBackend:
    '''
    Classe base para executar a ativação e desativação dos usuários
    '''
    def activating(self, user, *args, **kwargs):
        return user

    def deactivating(self, user, *args, **kwargs):
        return user




def exe_backends(user, *args, is_activating=None):
    '''
    Função que executará os backends em cascata e retornará o usuário
    '''
    backend_list = load_account_validaton_settings({}).get('backends')

    if not backend_list:
        raise AttributeError('Defina os backends desejados para a validação de conta')

    for backend in backend_list:

        _class = import_string(backend)

        if isinstance(_class(), BasicBackend):
            if is_activating:
                user = _class().activating(user,*args)
            else:
                user = _class().deactivating(user, *args)
        else:
            raise TypeError(f"A classe não herda a BasicHandle")
    return user
        
from nocton.account_validation.backends import BasicBackend

class DesactiveUser(BasicBackend):
    '''
    Classe simples para o caso de só querer desativar o usuário mesmo (claro, pensando no caso de usar algum auth_model com o campo is_active)
    '''
    def activating(self, user, *args, **kwargs):
        user.is_active = True
        return user
    
    def deactivating(self, user, *args, **kwargs):
        user.is_active = False
        return user
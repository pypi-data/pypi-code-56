from rest_framework.views import APIView, Response
from rest_framework import status
from nocton.account_validation.models import AccountValidatorToken
from nocton.account_validation.tools import validation_enable
from nocton.tools.console import print_f
from nocton.generics.exceptions import BAD_REQUEST

'''
    View feita para a validação de conta
'''
class ValidateAccount(APIView):
    def post(self, request, *args, **kwargs):
        activation_token = request.data.get('activation_token')

        # Se o token tiver sido enviado
        if activation_token:
            try:
                activation_token = AccountValidatorToken.objects.get(key=activation_token)
                user = activation_token.user

                # Ao deletar o token, automaticamente o usuário será ativo
                activation_token.delete()

                # Retorna informações básicas do usuário
                return Response({
                    "user_pk": user.pk,
                    'username': user.username,
                })
                
                
            except AccountValidatorToken.DoesNotExist:
                raise BAD_REQUEST('Senha de ativação inválida')
        else:
            raise BAD_REQUEST('Envie uma senha de autenticação')
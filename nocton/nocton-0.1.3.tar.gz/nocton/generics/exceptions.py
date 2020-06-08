from rest_framework.exceptions import APIException

'''
    APIException básica para padronização
'''
class Basic_APIException(APIException):
    def __init__(self, message):
        self.detail = message

'''
    Exceção de BAD_REQUEST
'''
class BAD_REQUEST(Basic_APIException):
    status_code = 400

'''
    Exceção de não encontrado
'''
class NOT_FOUND(Basic_APIException):
    status_code = 404

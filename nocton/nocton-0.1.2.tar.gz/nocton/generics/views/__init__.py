from .core_views import *

class List_View(List):
    '''
    Lista as informações relacionadas ao usuário (se tiver um user_relation) ou o queryset padrão. Caso o self_user estiver True, utiliza como principal usuário o request.user, caso não, tenta pega o usuário especificado na url.
    '''
    pass
    # def get(self, *args, **kwargs):
    #     return super().get_safe_GET(*args, **kwags)


class List_Create_View(List, generics.CreateAPIView):
    '''
    Faz o mesmo da List_View, mas permite criar uma nova instancia
    '''
    pass
    # def post(self, *args, **kwargs):
    #     return super().get_safe_POST(*args, **kwargs)



class Read_View(Generic_View, Retrieve):
    '''
    Como um RetrieveAPIView normal, mas o objeto vai ser procurado no queryset inicial, isto é, pode ficar em função de um user_relations e do usuário especificado na url.
    '''
    pass
    # def get(self, *args, **kwargs):
    #     return super().get_safe_GET(*args, **kwargs)


class Update_View(Generic_View, Update):
    '''
    Como um UpdateAPIView normal, mas o objeto vai ser procurado no queryset inicial, isto é, pode ficar em função de um user_relations e do usuário especificado na url.

    Também possui um campo always_partial que permite que as requisições utilizem put parcialmente.
    '''
    pass
    # def put(self, *args, **kwargs):
    #     return super().get_safe_PUT(*args, **kwargs)
    
    # def patch(self, *args, **kwargs):
    #     return super().get_safe_PATCH(*args, **kwargs)


class Delete_View(Generic_View, Delete):
    '''
    Como um DestroyAPIView normal, mas o objeto vai ser procurado no queryset inicial, isto é, pode ficar em função de um user_relations e do usuário especificado na url.
    '''
    pass


class Read_Update_View(Read_View, Update_View):
    pass

class Read_Delete_View(Read_View, Delete_View):
    pass

class Update_Delete_View(Update_View, Delete_View):
    pass

class Read_Update_Delete_View(Read_View, Update_View, Delete_View):
    pass


class Read_SingleRelated_View(Generic_SingleRelated_view, Retrieve):
    '''
    Como um RetrieveAPIView normal, mas com o objeto principal sendo o usuário ou algum objeto relacionado o usuário. O usuário também pode ser especificao através do campo self_user e da url (<int:user_pk>)
    Também permite filtrar os campos que devem ser mostrados
    '''
    pass
    # def get(self, *args, **kwargs):
    #     return super().get_safe_GET(*args, **kwargs)

class Update_SingleRelated_View(Generic_SingleRelated_view, Update):
    '''
    Como um UpdateAPIView normal, mas com o objeto principal sendo o usuário ou algum objeto relacionado o usuário.
    Também possibilita que as put's sejam parciais.
    '''
    pass
    # def put(self, *args, **kwargs):
    #     return super().get_safe_PUT(*args, **kwargs)
    
    # def patch(self, *args, **kwargs):
    #     return super().get_safe_PATCH(*args, **kwargs)


class Delete_SingleRelated_View(Generic_SingleRelated_view, Delete):
    '''
    Como um DeleteAPIView normal, mas com o objeto principal sendo o usuário ou algum objeto relacionado o usuário
    '''
    # def delete(self, *args, **kwargs):
    #     return super().get_safe_DELETE(*args, **kwargs)
    


class Read_Update_SingleRelated_View(Read_SingleRelated_View, Update_SingleRelated_View):
    pass

class Read_Delete_SingleRelated_View(Read_SingleRelated_View, Delete_SingleRelated_View):
    pass

class Update_Delete_SingleRelated_View(Update_SingleRelated_View, Delete_SingleRelated_View):
    pass

class Read_Update_Delete_SingleRelated_View(Read_SingleRelated_View, Update_SingleRelated_View, Delete_SingleRelated_View):
    pass
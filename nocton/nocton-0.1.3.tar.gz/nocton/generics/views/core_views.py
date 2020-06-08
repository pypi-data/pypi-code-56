from rest_framework import generics, status
from rest_framework.views import Response
from rest_framework.permissions import IsAuthenticated
from django.core.exceptions import FieldError, FieldDoesNotExist
from django.db.models.query import QuerySet
from django.contrib.auth import get_user_model
from nocton.tools import print_f
from nocton.tools import delete_from_dict, check_related
from nocton.generics.exceptions import NOT_FOUND


class Visualizer:
    '''
        Classe base com métodos que aplicam o filtro de atributos 
    '''

    exclude_attrs = []

    # Retorna os atributos a serem excluídos
    def get_exclude_attrs(self, *args, **kwargs):
        return self.exclude_attrs

    # Exclui os atributos
    def delete_attrs(self, default_item, *args, **kwargs):   
        exclude = self.get_exclude_attrs(*args, **kwargs)

        for attr in exclude:
            if isinstance(attr, str):
                # print(attr)
                default_item.pop(attr)

            else:
                delete_from_dict(default_item, attr)
        return default_item


class Basic_Generic(generics.GenericAPIView):
    '''
        Tenta, por padrão, colocar como usuário principal o usuário que for encontrado com a url <int:user_pk>; caso self_user seja especificado, coloca como usuário principal o request.user
    '''
    
    reference_object_relation = None
    reference_object_url_field = None
    reference_object_lookup = 'pk'
    automatic_self_user = None
    
    reference_object_model = get_user_model()

    # Retorna o objeto de referência
    def get_reference_object(self, *args, **kwargs):
        '''
        O objeto de referencia padrão é o usuário
        '''
    
        assert(
            self.automatic_self_user != None 
        ), 'Defina se você quer que o self_user seja automaticamente o objeto de referencia'

        # Caso automatic_self_user seja True, o objeto de referência se torna o usuário
        if self.automatic_self_user:
            _object = self.request.user

        # Caso não, será aplicada lógica para entrar o objeto de referência
        else:
            assert(
                self.reference_object_url_field
            ), 'Para encontrar um objeto principal específico, defina o reference_object_url_field e o reference_object_model ou sobreponha o método get_reference_object'

            # Tenta pegar o objeto de referência pela url (por um id ou algo assim)

            _object_model = self.reference_object_model
            _object_pk = self.request.resolver_match.kwargs[self.reference_object_url_field]
            _object_lookup_field = self.reference_object_lookup

            try:
                url_object = _object_model.objects.get(**{_object_lookup_field: _object_pk})
            except _object_model.DoesNotExist:
                raise NOT_FOUND(f'Não existe nenhum {_object_model.__name__} com {_object_lookup_field} = {_object_pk}')

            _object = url_object

            
        return _object

    # Retorna um atributo do objeto de referência especificado no reference_object_relation
    def get_reference_object_relation(self, _object, *args, **kwargs):
        return getattr(_object, self.reference_object_relation)


class Generic_View(Basic_Generic):
    '''
        O queryset inicial, que pode ser sobreposto, retorna, ou um queryset em função do usuário como especificado no campo de user_relation, ou retorna o queryset padrão.
    '''               

    # Retorna o queryset
    def get_queryset(self, *args, **kwargs):
        
        # Caso haja uma relação com o objeto de referência, retorna o atributo correspondente a essa relação
        if self.reference_object_relation:
            _object = self.get_reference_object(*args, **kwargs)
            _object_data = self.get_reference_object_relation(_object, *args, **kwargs)
            try:
                # checa se esse atributo pode se tornar um queryset
                _object_related_queryset = _object_data.all()
            except AttributeError as error:
                raise AttributeError(f"{error}; As relações com o usuário precisam ser de OneToMany ou ManyToMany, para ter um OneToOne é necessário customizar o método get_queryset")
            return _object_related_queryset

        # Caso não haja, retorna o queryset padrão
        else:
            # Checa se o queryset existe 
            try:
                return self.queryset.all()
            except AttributeError as error:
                raise AttributeError(f"A view não tem um queryset padrão: {error}")



class Generic_SingleRelated_view(Basic_Generic):
    '''
    APIView genérica que pega, como objeto o user ou algum objeto relacionado ao user, como um profile ou algo assim.
    '''

    def get_object(self, *args, **kwargs):
        _object = self.get_reference_object(*args, **kwargs)
        
        # Caso haja uma relação com o objeto de referência, tenta retornar o atributo correspondente a essa relação
        if self.reference_object_relation:
            _object_data = self.get_reference_object_relation(_object, *args, **kwargs)

            _object_related_data = _object_data
            # Checa se o objeto não é um queryset
            try:
                _object_related_data.all()

                raise TypeError('O tipo de relação com o model de users precisa ser de OneToOne')
            except AttributeError:
                return _object_related_data

        # Caso não haja essa relação, retorna o objeto em si
        else:
            return _object






class Retrieve(generics.RetrieveAPIView, Visualizer):
    '''
        Versão do NOCTON da RetrieveView padrão
    '''

    def retrieve(self, request, *args, **kwargs):
        # Aplica o objeto formatado
        item = super().retrieve(request, *args, **kwargs).data
        clear_item = self.delete_attrs(item, *args, **kwargs)
        
        return Response(clear_item)


class Update(generics.UpdateAPIView):
    '''
        Versão do NOCTON da UpdateView padrão
    '''

    always_partial = None

    # Tenta dar update no objeto, caso always_partial seja True, permite um update parcial
    def put(self, *args, **kwargs):
        if self.always_partial:
            return self.partial_update(*args, **kwargs)
        return super().put(*args, **kwargs)


class Delete(generics.DestroyAPIView):
    '''
        Versão do NOCTON da DeleteView padrão
    '''
    pass



class List(Visualizer, generics.ListAPIView, Generic_View):
    '''
    Lista as todos os itens especificados no user_relations em função do usuário logado. Caso a relação não retorne um queryset, retorna um erro.
    Caso o user_relations não seja especificado, retorna o a lista especificada no queryset.

    A classe também tem dois métodos adicionais. Seach, que usa o campo searching, e o ordinate, que utiliza o campo order. Por padrão todas as pesquisas são ordenadas pelo pk.
    '''

    # permission_classes = [IsAuthenticated]
    searching = []
    order = ['-pk']


    # Retorna o queryset que será usado na listagem
    def get_queryset(self, *args, **kwargs):
        # Filtra o queryset         
        searched_queryset = self.search(
            *args,
            queryset=super().get_queryset(*args, **kwargs),
            query_params=self.request.query_params,
            **kwargs
        )

        # Ordena o queryset
        ordinated_queryset = self.ordinate(
            *args,
            queryset=searched_queryset,
            query_params=self.request.query_params,
            **kwargs
        )

        return ordinated_queryset


    # Aplica o filtro de campos caso não esteja com paginação, caso esteja, ignora essa etapa
    def list(self, request, *args, **kwargs):
        default_list = super().list(request, *args, **kwargs)
        queryset = self.get_queryset()

        is_paginated = self.paginate_queryset(queryset)
        
        # Checa se está com paginação
        if is_paginated is not None:
            return default_list

        else:
            clear_list = list()

            # Aplica a paginação
            for item in default_list.data:
                clear_list.append(self.delete_attrs(item, request, *args, **kwargs))

            return default_list


    # Aplica o filtro de informações
    def search(self, *args, **kwargs):
        query_params = kwargs.get('query_params', self.request.query_params)
        queryset = kwargs.get('queryset', super().get_queryset(*args, **kwargs))


        for searching_field in self.searching:
            if isinstance(searching_field, str):
                field_name = search_name = searching_field
                endding = 'icontains'
            else:
                field_name = searching_field.get('field_name')
                search_name = searching_field.get('search_name', field_name)
                endding = searching_field.get('endding', 'icontains')


            try:
                if query_params.get(search_name):
                    if not field_name:
                        raise SyntaxError('O dicionário de pesquisa deve apresentar ao menos o "field_name"')

                    _filter = {
                        f"{field_name}__{endding}": query_params.get(search_name)
                    }
                    queryset = queryset.filter(**_filter)

            except FieldError as error:
                print_f("Ocorreu um erro durante o filtro de informações:", error)

        return queryset


    # Ordena o queryset
    def ordinate(self, *args, **kwargs):
        queryset = kwargs.get('queryset', super().get_queryset(*args, **kwargs))

        queryset = queryset.order_by(*self.order)
        return queryset



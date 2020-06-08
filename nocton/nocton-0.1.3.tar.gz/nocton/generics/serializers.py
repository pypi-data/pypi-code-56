from rest_framework import serializers
import json

# Serializer que facilita a representação de campos
class ModelSerializer(serializers.ModelSerializer):
    # ...

    def to_representation(self, instance):
        # Pega a representação padrão
        default_representation = super().to_representation(instance)
        representation = default_representation

        for field_name in default_representation:
            # Se houver um método com o nome do campo, o campo passa a ter o valor dele
            try:
                field_method = getattr(self, f"get_{field_name}")    
                representation[field_name] = field_method(instance)
            
            # Se não, passa
            except AttributeError:
                pass

        return representation




class ArrayField(serializers.Field):
    # Retorna o value cru mesmo
    def to_representation(self, value):
        return value


    def to_internal_value(self, data):
        if isinstance(data, list):
            return data
        
        elif isinstance(data, str):
            # Caso data esteja relativamente mal formatado
            if not (data[0] == '[' and data[-1] == ']'):
                data = f"[{data}]"
                
            json_data = json.loads(data)
            return json_data

        # Não aceita outros tipos de dados
        else:
            serializers.ValidationError('Esse campo deve enviar um array ou uma string no formato de um array: [item_1, item_2 ...]')

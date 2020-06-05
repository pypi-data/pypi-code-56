{% load code_generator_tags %}from rest_framework.serializers import ModelSerializer

{% models_imports app models %}
{% for model in models %}

class {{model.name}}Serializer(serializers.ModelSerializer):
    class Meta:
        model = {{model.name}}
        fields = ({% serializers_fields model.serializer_field_names %},)
{% endfor %}
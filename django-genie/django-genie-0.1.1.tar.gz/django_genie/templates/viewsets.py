{% load code_generator_tags %}from rest_framework import permissions
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.viewsets import ModelViewSet

{% models_imports app models %}

{% serializers_imports app models %}
{% for model in models %}

class {{model.name}}ViewSet(ModelViewSet):
    serializer_class = {{model.name}}Serializer
    queryset = {{model.name}}.objects.all()
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user.id, updated_by=self.request.user.id)

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user.id)
{% endfor %}
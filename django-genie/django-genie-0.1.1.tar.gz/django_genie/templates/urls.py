{% load code_generator_tags %}from django.urls import path, include
from rest_framework import routers

{% views_imports app models %}

app_name = '{{app}}'

router = routers.DefaultRouter()

urlpatterns = [
    {% for model in models %}path('{{model.snake_case_name}}s', {{model.name}}CRUDView.as_view(), name='{{model.snake_case_name}}_crud'),
    {% endfor %}
]
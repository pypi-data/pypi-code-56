{% load code_generator_tags %}from django.shortcuts import render
from django.views import View
{% for model in models %}

class {{model.name}}CRUDView(View):
    template_name = "{{app}}/{{model.snake_case_name}}.html"

    def get(self, request):
        return render(request, '{{app}}/{{model.snake_case_name}}.html')
{% endfor %}
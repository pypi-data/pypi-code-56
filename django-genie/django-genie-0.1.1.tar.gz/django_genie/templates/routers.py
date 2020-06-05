# api_router imports
{% load code_generator_tags %}{% viewsets_imports app models %}

# Router register code
{% for model in models %}router.register("{{model.snake_case_name}}", {{model.name}}ViewSet)
{% endfor %}
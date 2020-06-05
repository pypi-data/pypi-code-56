{% load code_generator_tags %}from django.contrib import admin
from reversion.admin import VersionAdmin

{% models_imports app models %}
{% for model in models %}

@admin.register({{model.name}})
class {{model.name}}Admin(VersionAdmin):
    """Admin class for {{model.name}}"""

    exclude = ('created_by', 'updated_by', 'deleted_at')
    list_display = ({% admin_list_display_fields model.admin_field_names %},)
    list_filter = ('updated_at',)
    ordering = ()      # Add your required fields here
    search_fields = () # Add your required fields here

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.created_by = request.user.id
        obj.updated_by = request.user.id
        super().save_model(request, obj, form, change)
{% endfor %}
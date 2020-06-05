from django import template
from django.utils.safestring import mark_safe

register = template.Library()
project = "" # Add your django project name


@register.simple_tag()
def models_imports(app, models):
    return mark_safe(
        "\n".join(["from {}.{}.models.{} import {}".format(project, app, app, model.name) for model in models])
    )


@register.simple_tag()
def serializers_fields(fields_list):
    return mark_safe(fields_list)


@register.simple_tag()
def serializers_imports(app, models):
    return mark_safe(
        "\n".join(["from {}.{}.api.serializers import {}Serializer".format(project, app, model.name) for model in models])
    )


@register.simple_tag()
def views_imports(app, models):
    return mark_safe(
        "\n".join(["from {}.{}.views.{} import {}CRUDView".format(project, app, app, model.name) for model in models])
    )


@register.simple_tag()
def admin_list_display_fields(fields_list):
    return mark_safe(fields_list)


@register.simple_tag()
def viewsets_imports(app, models):
    return mark_safe(
        "\n".join(["from {}.{}.api.views import {}ViewSet".format(project, app, model.name) for model in models])
    )

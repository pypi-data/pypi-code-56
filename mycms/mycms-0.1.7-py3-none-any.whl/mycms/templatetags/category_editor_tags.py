from django import template
register = template.Library()

    
@register.inclusion_tag('mycms/templatetags/category_editor.html', takes_context=True)
def category_editor(context, *args, **kwargs):
    
    script_list =context.get("script_list", [])
    return { "script_list": script_list}
    
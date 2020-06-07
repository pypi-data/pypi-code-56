from django import template

from mycms.models import CMSEntries

register = template.Library()


@register.tag
def PageNavigation(parser, token):
    
    return PageNavigationNode()


class PageNavigationNode(template.Node):
    
    def __init__(self):
        pass
    
    def render(self, context):
        #Load the template and return it 
        self.request = template.Variable('request')
        t = template.loader.get_template("mycms/templatetags/PageNavigation.html")
    
        return t.render(context.flatten())


@register.tag
def MemberPageNavigation(parser, token):
    
    return MemberPageNavigationNode()

class MemberPageNavigationNode(template.Node):
    
    def __init__(self):
        
        pass
    
    def render(self, context):
        
        self.request = template.Variable('request')
        t = template.loader.get_template("mycms/templatetags/MemberPageNavigation.html")
        return t.render(context.flatten())

        
        
@register.inclusion_tag('mycms/templatetags/widgets/categories.html')
def categories_widget():
    """Get all the categories for the current page."""
    
    return {}


@register.inclusion_tag('mycms/templatetags/widgets/base_categories.html')
def base_categories_widget(cols):
    """Get all the categories for the current page."""

    def row_objects(obj_list):
        for i in range(0, len(obj_list), cols):
            yield obj_list[i:i +cols]

    obj_list = CMSEntries.objects.filter(path__parent__path = "/",
                                         page_type__page_type="CATEGORY")   

    
    return {"categories": obj_list, "row_objects": row_objects(obj_list)}
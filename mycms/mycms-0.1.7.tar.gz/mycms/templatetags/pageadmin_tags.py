from django import template


register = template.Library()


@register.tag
def PageAdmin(parser, token):
    
    return PageAdminNode()


class PageAdminNode(template.Node):
    
    def __init__(self):
        pass
    
    def render(self, context):
        #Load the template and return it 
        self.request = template.Variable('request')
        self.request.jason = "monkey"
        t = template.loader.get_template("mycms/templatetags/PageAdmin.html")
    
        return t.render(context.flatten())
        
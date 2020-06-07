from django import template
from django.core.exceptions import ObjectDoesNotExist
from django.template import Template, Context
from django.template.loader import get_template
from django.contrib.auth.models import User
from django.core.paginator import Paginator


from django.template.loader import render_to_string

#from mycms.models import Paths, Pages
#from mycms.pageview.base import get_pageview

from mycms.models import  CMSPaths
from mycms.models import CMSEntries

register = template.Library()

@register.inclusion_tag('mycms/templatetags/widgets/categories_menu.html')
def categories_menu():
    """
    Used to get a full category tree starting from /cms/. 
    """
    
    try:
        parent = CMSEntries.objects.get(path__path="/")
    except ObjectDoesNotExist as e:
        msg = "No CMSEntries to produce full_menu from /. Perhaps / does not yet exist!!"
        logger.fatal(msg)
        parent = None
    return {"parent":parent}


@register.inclusion_tag('mycms/templatetags/widgets/google_adds.html')
def google_adds():
    
    return { "width": 300, "height": 600, "add-client": "data=ca-pub-9449210019187312", "data-ad-slot":"6783855847"}


@register.inclusion_tag('mycms/templatetags/widgets/search.html')
def search():
    return {}

@register.inclusion_tag('mycms/templatetags/widgets/google_adds.html')
def addsbygoogle():
    
    return { "width": 300, "height": 600, 
             "add-client": 
             "data=ca-pub-9449210019187312", 
             "data-ad-slot":"6783855847",
             "data-ad-format":"auto",
             "data-full-width-responsive":"true"}
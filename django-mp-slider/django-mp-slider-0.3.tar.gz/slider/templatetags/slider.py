
from django import template
from django.conf import settings

from slider.models import SliderImage


register = template.Library()


@register.inclusion_tag('slider.html')
def render_slider():
    return {'slider_photos': SliderImage.objects.all()}


@register.inclusion_tag('slideshow.html')
def render_slideshow(images, preview_size=None):
    return {
        'MEDIA_URL': settings.MEDIA_URL,
        'images': images,
        'preview_size': preview_size
    }


@register.inclusion_tag('slideshow_js.html', name='slideshow_js')
def render_slideshow_js(group_name='slideshow'):
    return {
        'STATIC_URL': settings.STATIC_URL,
        'group_name': group_name
    }

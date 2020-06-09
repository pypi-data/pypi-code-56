from django import forms
from django.contrib import admin
from django.urls.resolvers import get_resolver, RegexPattern, URLPattern, URLResolver
from django.conf import settings

from .models import Tip


def url_choices(resolver, namespace=None):
    choices = []
    try:
        for entry in resolver.url_patterns:
            if isinstance(entry, RegexPattern) or isinstance(entry, URLPattern):
                if not entry.name:
                    continue
                    name = entry.lookup_str
                    pkg, viewname = name.rsplit('.', 1)
                    choices.append((name, viewname))
                elif namespace:
                    name = '%s:%s' % (namespace, entry.name)
                    choices.append((entry.name, name))
                else:
                    choices.append((entry.name, entry.name))
            elif isinstance(entry, URLResolver):
                if namespace and entry.namespace:
                    ns = '%s:%s' % (namespace, entry.namespace)
                else:
                    ns = entry.namespace or namespace
                if ns not in getattr(settings, 'TOTD_EXCLUDE_NS', []):
                    choices.extend(url_choices(resolver=entry, namespace=ns))
    except Exception as e:
        print("URL lookup failed: %s" % e)
        pass
    return choices


# Register your models here.
class TipForm(forms.ModelForm):
    class Meta:
        model = Tip
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        choices = [("", "-- All Pages --")]
        choices.extend(url_choices(get_resolver(None)))

        self.fields["view"].widget = forms.Select(choices=choices)


class TipAdmin(admin.ModelAdmin):
    list_filter = ("level", "view")
    list_display = ("name", "level", "view", "run_start", "run_end", "seen_count")
    search_fields = ("name", "view")
    form = TipForm

    def seen_count(self, tip):
        return tip.seen_by.count()

    seen_count.short_description = "Seen by"


admin.site.register(Tip, TipAdmin)

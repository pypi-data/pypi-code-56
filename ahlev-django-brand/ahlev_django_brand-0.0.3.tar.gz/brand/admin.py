from django.contrib import admin
from django.utils.html import format_html
from .models import Brand

class BrandAdmin(admin.ModelAdmin):

    search_fields = ['name']

    list_display = ['name', 'preview_logo', 'date_created', 'last_updated']

    fieldsets = [
        (None, {
            'fields': ['name', 'logo'],
        }),
    ]

    def preview_logo(self, obj):
        return format_html("<img src='/medias/{}' style='height: 50px;'/>".format(obj.logo))
    preview_logo.admin_order_field = 'name'
    preview_logo.short_description = 'logo'

    readonly_fields =  [ 'preview_logo' ]


admin.site.register(Brand, BrandAdmin)
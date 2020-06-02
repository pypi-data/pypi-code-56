from django.contrib import admin
from django.core.exceptions import ImproperlyConfigured
from django.urls import path, reverse
from django.utils.translation import gettext_lazy as _
from .models import ImportJob
from .views.importview import ImportView, ImportConfirmView
from . import default_registry


class IssuesAdminMixin:
    def get_list_filter(self, request):
        return [
            *super().get_list_filter(request),
            IssueFilter
        ]


class ImportAdminMixin:
    def changelist_view(self, request, extra_context=None, **kwargs):
        return super().changelist_view(
            request,
            extra_context={
                'import_url': reverse('admin:{}'.format(self.__admin_name('import'))),
            },
            **kwargs
        )


    def get_urls(self):
        def wrap(view_class):
            return self.admin_site.admin_view(view_class.as_view(
                model=self.model,
                staging_model=self.staging_model
            ))

        return [
            path('import/', wrap(ImportView), name=self.__admin_name('import')),
            path('import/<int:job_id>', wrap(ImportConfirmView), name=self.__admin_name('import_confirm')),
            *super().get_urls(),
        ]

    def __admin_name(self, name):
        return '{}_{}_{}'.format(self.model._meta.app_label, self.model._meta.model_name, name)


class IssueFilter(admin.SimpleListFilter):
    template = 'masterdata/filter.html'
    title = _('Data Quality Issues')

    parameter_name = 'check'

    def __init__(self, request, params, model, model_admin):
        if model not in default_registry:
            raise ImproperlyConfigured('IssueFilter couldn\'t find model {} in the registry'.format(model.__name__))
        self.model_registry = default_registry[model]
        super().__init__(request, params, model, model_admin)

    def lookups(self, request, model_admin):
        return (
            (alias, issuecount)
            for alias, issuecount in self.model_registry.gen_aliased_issue_counts()
        )

    def queryset(self, request, queryset):
        for ref, check in self.model_registry.get_aliased_checks():
            if ref == self.value():
                return check.filter(queryset)
        return queryset


admin.site.register(ImportJob)

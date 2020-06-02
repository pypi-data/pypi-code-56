from django.http import HttpResponse, HttpResponseRedirect
from django.forms import Form, CharField, Textarea
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views.generic.base import View, TemplateView, ContextMixin
from masterdata.importing import ModelImporter
from masterdata.models import ImportJob
import io
import json


class ImportForm(Form):
    data = CharField(
        widget=Textarea,
        help_text=_('Copie y pegue el texto desde una planilla Excel')
    )


class ImportView(View):
    model = None
    staging_model = None

    def get(self, request):
        return render(
            request,
            'masterdata/import_form.html',
            context={
                'opts': self.model._meta,
                'form': ImportForm(),
            }
        )

    def post(self, request):
        stream = io.StringIO(request.POST['data'])
        job = ImportJob.objects.create()
        results = ModelImporter(
            model=self.staging_model,
            data=lambda data: {**data, 'job': job}
        ).import_tsv(stream)

        job.created = results.created
        job.updated = results.updated
        job.errors = results.errors
        job.status = ImportJob.Status.COMPLETED
        job.save()

        return HttpResponseRedirect(reverse(
            'admin:{}_{}_{}'.format(
                self.model._meta.app_label,
                self.model._meta.model_name,
                'import_confirm'
            ),
            args=(job.id,)
        ))


class ImportConfirmView(View):
    model = None
    staging_model = None
    template_name = 'masterdata/import_confirm.html'

    def get(self, request, job_id):
        return render(
            request,
            'masterdata/import_confirm.html',
            context={
                'opts': self.model._meta,
                'job': get_object_or_404(ImportJob, pk=job_id),
            }
        )

    def post(self, request, job_id):
        job = get_object_or_404(ImportJob, pk=job_id)
        action = request.POST['action']

        handlers = {
            'publish': lambda: publish_staged_models(job, self.staging_model, self.model),
            'cancel': lambda: cancel_importjob,
        }

        if action not in handlers:
            return HttpResponse(f'Unsupported action: {action}', status_code=409)

        handlers[action]()

        return HttpResponseRedirect(reverse(
            'admin:{}_{}_{}'.format(
                self.model._meta.app_label,
                self.model._meta.model_name,
                'changelist'
            )
        ))


def publish_staged_models(job, staging_model, target_model):
    target_objs = (
        target_model(**{
            field.name: getattr(obj, field.name)
            for field in target_model._meta.local_fields
        })
        for obj in job.staged_objects.all()
    )

    target_model.objects.bulk_create(target_objs)

def cancel_importjob(job):
    print(job)




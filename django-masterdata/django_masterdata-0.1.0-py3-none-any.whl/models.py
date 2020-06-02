from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.translation import gettext_lazy as _
import importlib
from . import default_registry


class Issue(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    obj_id = models.PositiveIntegerField()
    obj = GenericForeignKey('content_type', 'obj_id')
    check = models.CharField(max_length=255)


class ImportJob(models.Model):
    class Status(models.TextChoices):
        STARTED = _('Started')
        COMPLETED = _('Completed')

    created_at = models.DateTimeField(auto_now_add=True)
    created = models.SmallIntegerField(null=True, blank=True)
    updated = models.SmallIntegerField(null=True, blank=True)
    errors = models.SmallIntegerField(null=True, blank=True)


class StagedBaseModel(models.Model):
    class Meta:
        abstract = True

    job = models.ForeignKey(ImportJob, null=True, on_delete=models.SET_NULL, related_name='staged_objects')


class StagingMetaClass(type(models.Model)):
    def __new__(cls, clsname, bases, attrs, registry=None):
        if clsname == 'StagingModel':
            return super().__new__(cls, clsname, bases, attrs)

        if registry is None:
            registry = default_registry

        target = attrs.pop('target')
        for field in target._meta.local_fields:
            if isinstance(field, models.AutoField):
                continue
            name, importpath, args, kwargs = field.deconstruct()
            parentpath, _ , classname = importpath.rpartition('.')
            field_class = getattr(importlib.import_module(parentpath), classname)
            kwargs['null'] = True
            attrs[name] = field_class(*args, **kwargs)

        return super().__new__(cls, clsname, (StagedBaseModel,), attrs)


class StagingModel(metaclass=StagingMetaClass):
    pass

import csv
import json

import re
from django.apps import apps
from django.db.models import Model
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.core.serializers.json import DjangoJSONEncoder
from itertools import chain

lookup_re = re.compile(
    r'^(?P<target_field>\w+)'
    r'(?P<op>[\+@])(?P<app_label>\w+)\.'
    r'(?P<model_name>\w+)\.'
    r'(?P<lookup_field>\w+)$'
)


BATCH_SIZE = 500


class CreateAction:
    pass


class UpdateAction:
    pass


class ErrorAction:
    pass


class ModelImporter:
    '''Implements importing data from CSV style files,
    with a preference for TSV files with headers,
    into Django Models'''

    def __init__(
        self, model,
        key=None, field_specs=None, skip_header=0, data=None
    ):
        self.model = _resolve_model(model)
        self.key = _resolve_key(key)
        self.data = data or (lambda data: data)
        self.field_specs = field_specs
        self.skip_header = skip_header

    def import_tsv(self, fh, quiet=False, skip_errors=False, **tsv_options):
        '''Imports from a TSV file with optional quotes (") delimiting text fields
        '''
        results = sum(
            (
                self.bulk_operate(batches)
                for batches in self.iter_batches(
                    self.iter_rows(fh, skip_errors, **tsv_options)
                )
            ),
            start=ImportResults()
        )
        return results

    def iter_rows(self, fh, skip_errors, **tsv_options):
        '''Reads CSV rows from a file-like object and yields
        data dicts'''

        dialect = _csv_dialect(**tsv_options)

        field_specs = self.field_specs or next(csv.reader(fh, dialect=dialect))

        assert len(set(field_specs)) == len(field_specs), 'Duplicate field specs not allowed'

        field_resolvers = [
            field_resolver(spec)
            for spec in field_specs
        ]

        for i, row in enumerate(csv.DictReader(fh, fieldnames=field_specs, dialect=dialect)):
            if None in row:
                del row[None]

            if i < self.skip_header:
                continue

            data = None
            try:
                data = self.data({
                    field: resolver(value)
                    for (field, resolver), value in zip(
                        field_resolvers,
                        row.values()
                    )
                    if not field.startswith('_')
                })

                if self.key:
                    try:
                        obj = self.model.objects.get(
                            **{k: data[k] for k in self.key}
                        )
                        obj = self.model(**data, pk=obj.pk)
                        obj.full_clean(validate_unique=False)
                        yield UpdateAction, (obj, data.keys())
                        continue
                    except ObjectDoesNotExist:
                        pass

                obj = self.model(**data)
                obj.full_clean()
                yield CreateAction, obj

            except Exception as e:
                if not skip_errors:
                    raise e
                yield ErrorAction, (e, data)

    def iter_batches(self, actions):
        batches = {
            CreateAction: [],
            UpdateAction: [],
            ErrorAction: [],
        }

        def reset():
            for b in batches.values():
                b.clear()

        for i, (action, args) in enumerate(actions, start=1):
            batches[action].append(args)
            if i % BATCH_SIZE == 0:
                yield batches
                reset()
        yield batches

    def bulk_operate(self, batches):
        '''Gathers actions from an iterator and performs bulk operations
        on it'''
        r = ImportResults()

        objs = batches[CreateAction]
        try:
            self.model.objects.bulk_create(objs)
            r.created += len(objs)
        except Exception as e:
            r.errors += len(objs)
            r.addError(e, objs)

        if batches[UpdateAction]:
            objs = [args[0] for args in batches[UpdateAction]]
            fields = batches[UpdateAction][0][1]

            try:
                self.model.objects.bulk_update(objs, fields)
                r.updated += len(batches[UpdateAction])
            except Exception as e:
                r.errors += len(batches[UpdateAction])
                r.addError(e, objs)

        errors = batches[ErrorAction]
        for e, data in errors:
            r.addError(e, data)
        r.errors += len(errors)

        return r


def field_resolver(fieldname):
    '''Para cada field de los encabezados del CSV se genera y retorna un par: fieldname, resolver
    El resolver es una función que convierte el valor del CSV en el valor que se quiere cargar a
    la BBDD.

    Un encabezado que requiere de lookups se puede especificar de la siguiente manera:

    <target_field>@<app>.<model>.<lookup_field>

    En este caso el valor del campo proveniente del CSV
    se busca en la BBDD dentro del modelo <app>.<model> en el campo
    <lookup_field>. El resultado se guardará en el campo <target_field>.
    '''
    match = lookup_re.match(fieldname)
    if match:
        field = match.group('lookup_field')
        op = match.group('op')
        model = apps.get_model(match.group('app_label'), match.group('model_name'))
        cache = {value: pk for value, pk in model.objects.values_list(field, 'pk')}

        def resolver(value):
            cached = cache.get(value)
            if cached:
                return cached
            else:
                return model.objects.get(**{field: value}).pk

        return match.group('target_field'), resolver

    else:
        def resolver(value):
            if value != '':
                return value
        return fieldname, resolver


def _resolve_model(model_spec):
    '''Retuns a Django Model class from:
        - An {app_label}.{model_name} string
    '''
    if issubclass(model_spec, Model):
        return model_spec
    app_label, model_name = model_spec.split('.')
    return apps.get_model(app_label, model_name)


def _resolve_key(key_spec):
    '''Returns a tuple representing a composite lookup key from:
        - A comma separated list 'field1,field2'
    '''
    if key_spec is None:
        return None
    return key_spec.split(',')


def _csv_dialect(**options):
    '''Returns a `csv` dialect with the given options.
    Defaults to the `csv.excel` dialect with '\t' delimiter and
    '"' quotechar
    '''
    class Dialect(csv.excel):
        delimiter = options.get('delimiter', '\t')
        quotechar = options.get('quotechar', '"')

    return Dialect


class ImportResults:
    def __init__(self, errors=0, created=0, updated=0, error_data=None):
        self.errors = errors
        self.created = created
        self.updated = updated
        self.error_data = error_data or []
        self.total = created + updated + errors

    def addError(self, error, data):
        self.error_data.append({'error': str(error), 'data': data})

    def __add__(self, other):
        return ImportResults(
            errors=self.errors + other.errors,
            created=self.created + other.created,
            updated=self.updated + other.updated,
            error_data=self.error_data + other.error_data,
        )

    def __str__(self):
        return json.dumps(
            {
                'total': self.total,
                'created': self.created,
                'updated': self.updated,
                'errors': self.errors,
            },
            cls=DjangoJSONEncoder
        )

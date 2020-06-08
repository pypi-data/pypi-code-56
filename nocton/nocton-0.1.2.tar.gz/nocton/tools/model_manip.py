from django.core.exceptions import FieldDoesNotExist
from django.db.models.fields import related


RELATED_CLASSES = [related.ForeignKey, related.OneToOneField, related.ManyToManyField]


def has_field(model, field_name):
    try:
        field = model._meta.get_field(field_name)
        return field
    except FieldDoesNotExist:
        return False

def in_objects(instance, model):
    queryset = model.objects.all()

    return instance in queryset



def check_related(model, field_name):
    db_field = has_field(model, field_name)

    if db_field:
        for field_class in RELATED_CLASSES:
            if isinstance(db_field, field_class):
                return True

    return False
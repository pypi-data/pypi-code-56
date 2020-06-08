from huscy.projects.filters import DataAcquisitionMethodFilter
from huscy.projects.models import DataAcquisitionMethod


def add_data_acquisition_method(session, type, location, order=None):
    if order is None:
        order = DataAcquisitionMethod.objects.filter(session=session).count() + 1

    return DataAcquisitionMethod.objects.create(
        session=session,
        type=type,
        location=location,
        order=order
    )


def get_data_acquisition_methods(project=None):
    qs = DataAcquisitionMethod.objects.order_by('pk')
    filters = dict(project=project and project.pk)
    return DataAcquisitionMethodFilter(filters, queryset=qs).qs

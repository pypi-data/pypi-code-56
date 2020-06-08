from django_filters import rest_framework as filters

from huscy.projects import models


class DataAcquisitionMethodFilter(filters.FilterSet):
    project = filters.NumberFilter(field_name='session__experiment__project', lookup_expr='exact')

    class Meta:
        model = models.DataAcquisitionMethod
        fields = (
            'project',
        )


class ExperimentFilter(filters.FilterSet):
    class Meta:
        model = models.Experiment
        fields = (
            'project',
        )

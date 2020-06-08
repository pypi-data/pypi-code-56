import pytest

from rest_framework.reverse import reverse
from rest_framework.status import HTTP_200_OK, HTTP_403_FORBIDDEN

from huscy.projects import services

pytestmark = pytest.mark.django_db


def test_admin_user_can_get_data_acquisition_methods(admin_client, data_acquisition_method):
    response = list_data_acquisition_methods(admin_client,
                                             data_acquisition_method.session.experiment.project)

    assert response.status_code == HTTP_200_OK


def test_user_without_permission_can_get_data_acquisition_methods(client, data_acquisition_method):
    response = list_data_acquisition_methods(client,
                                             data_acquisition_method.session.experiment.project)

    assert response.status_code == HTTP_200_OK


def test_anonymous_user_cannot_get_data_acquisition_methods(anonymous_client,
                                                            data_acquisition_method):
    response = list_data_acquisition_methods(anonymous_client,
                                             data_acquisition_method.session.experiment.project)

    assert response.status_code == HTTP_403_FORBIDDEN


def test_service_function_was_called(mocker, client, project):
    mocker.spy(services, 'get_data_acquisition_methods')

    list_data_acquisition_methods(client, project)

    services.get_data_acquisition_methods.assert_called_once_with(project)


def list_data_acquisition_methods(client, project):
    return client.get(reverse('project-dataacquisitionmethods', kwargs=dict(pk=project.pk)))

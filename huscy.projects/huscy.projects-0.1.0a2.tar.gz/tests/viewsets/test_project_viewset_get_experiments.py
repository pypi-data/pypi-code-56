import pytest

from rest_framework.reverse import reverse
from rest_framework.status import HTTP_200_OK, HTTP_403_FORBIDDEN

from huscy.projects import services

pytestmark = pytest.mark.django_db


def test_admin_user_can_get_experiments(admin_client, experiment):
    response = list_experiments(admin_client, experiment.project)

    assert response.status_code == HTTP_200_OK


def test_user_without_permission_can_get_experiments(client, experiment):
    response = list_experiments(client, experiment.project)

    assert response.status_code == HTTP_200_OK


def test_anonymous_user_cannot_get_experiments(anonymous_client, experiment):
    response = list_experiments(anonymous_client, experiment.project)

    assert response.status_code == HTTP_403_FORBIDDEN


def test_service_function_was_called(mocker, client, project):
    mocker.spy(services, 'get_experiments')

    list_experiments(client, project)

    services.get_experiments.assert_called_once_with(project)


def list_experiments(client, project):
    return client.get(reverse('project-experiments', kwargs=dict(pk=project.pk)))

import pytest

from rest_framework.reverse import reverse
from rest_framework.status import HTTP_201_CREATED, HTTP_403_FORBIDDEN

from huscy.projects import services

pytestmark = pytest.mark.django_db


def test_admin_user_can_create_experiments(admin_client, project):
    response = create_experiment(admin_client, project)

    assert response.status_code == HTTP_201_CREATED


def test_user_without_permission_can_create_experiments(client, project):
    response = create_experiment(client, project)

    assert response.status_code == HTTP_201_CREATED


def test_anonymous_user_cannot_create_experiments(anonymous_client, project):
    response = create_experiment(anonymous_client, project)

    assert response.status_code == HTTP_403_FORBIDDEN


@pytest.mark.skip
def test_service_function_was_called(mocker, client, project):
    mocker.spy(services, 'create_experiment')

    create_experiment(client, project)

    services.create_experiment.assert_called_once_with(project)


def create_experiment(client, project):
    return client.post(reverse('experiment-list'), data=dict(project=project.id))

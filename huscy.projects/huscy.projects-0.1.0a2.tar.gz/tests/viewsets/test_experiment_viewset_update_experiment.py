import pytest

from rest_framework.reverse import reverse
from rest_framework.status import HTTP_200_OK, HTTP_403_FORBIDDEN


def test_admin_user_can_update_experiments(admin_client, experiment):
    response = update_experiment(admin_client, experiment)

    assert_success(response)
    assert_experiment_is_updated(experiment)


def test_user_without_permission_can_update_experiments(client, experiment):
    response = update_experiment(client, experiment)

    assert_success(response)
    assert_experiment_is_updated(experiment)


@pytest.mark.django_db
def test_anonymous_user_cannot_update_experiments(anonymous_client, experiment):
    response = update_experiment(anonymous_client, experiment)

    assert_permission_denied(response)
    assert_experiment_not_updated(experiment)


def update_experiment(client, experiment):
    return client.put(
        reverse('experiment-detail', kwargs=dict(pk=experiment.pk)),
        data=dict(
            description='new description',
            order=experiment.order,
            project=experiment.project.pk,
            title='new title',
        )
    )


def assert_success(response):
    assert response.status_code == HTTP_200_OK


def assert_permission_denied(response):
    assert response.status_code == HTTP_403_FORBIDDEN


def assert_experiment_is_updated(experiment):
    experiment.refresh_from_db()
    assert 'new description' == experiment.description
    assert 'new title' == experiment.title


def assert_experiment_not_updated(experiment):
    experiment.refresh_from_db()
    assert 'description' == experiment.description

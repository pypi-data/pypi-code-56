import pytest

from rest_framework.reverse import reverse
from rest_framework.status import HTTP_204_NO_CONTENT, HTTP_403_FORBIDDEN

pytestmark = pytest.mark.django_db


def test_admin_user_can_delete_experiments(admin_client, experiment):
    response = delete_experiment(admin_client, experiment)

    assert response.status_code == HTTP_204_NO_CONTENT


def test_user_without_permission_can_delete_experiments(client, experiment):
    response = delete_experiment(client, experiment)

    assert response.status_code == HTTP_204_NO_CONTENT


def test_anonymous_user_cannot_delete_experiments(anonymous_client, experiment):
    response = delete_experiment(anonymous_client, experiment)

    assert response.status_code == HTTP_403_FORBIDDEN


def delete_experiment(client, experiment):
    return client.delete(reverse('experiment-detail', kwargs=dict(pk=experiment.pk)))

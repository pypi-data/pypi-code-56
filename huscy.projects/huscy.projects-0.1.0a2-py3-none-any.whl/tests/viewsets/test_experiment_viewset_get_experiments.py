from rest_framework.reverse import reverse
from rest_framework.status import HTTP_405_METHOD_NOT_ALLOWED


def test_retrieve_experiments_is_not_provided(client, experiment):
    response = retrieve_experiment(client, experiment)

    assert_method_not_allowed(response)


def test_list_experiments_is_not_provided(client):
    response = list_experiments(client)

    assert_method_not_allowed(response)


def retrieve_experiment(client, experiment):
    return client.get(reverse('experiment-detail', kwargs=dict(pk=experiment.pk)))


def list_experiments(client):
    return client.get(reverse('experiment-list'))


def assert_method_not_allowed(response):
    assert response.status_code == HTTP_405_METHOD_NOT_ALLOWED

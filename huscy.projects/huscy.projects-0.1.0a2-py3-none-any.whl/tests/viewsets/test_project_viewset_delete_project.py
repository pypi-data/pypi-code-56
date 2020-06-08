import pytest

from rest_framework.reverse import reverse
from rest_framework.status import HTTP_204_NO_CONTENT, HTTP_403_FORBIDDEN

from django.contrib.auth.models import Permission

from huscy.projects import services

pytestmark = pytest.mark.django_db


def test_admin_user_can_delete_projects(admin_client, public_project):
    response = delete_project(admin_client, public_project)

    assert response.status_code == HTTP_204_NO_CONTENT


def test_user_with_permission_can_delete_projects(client, user, public_project):
    delete_permission = Permission.objects.get(codename='delete_project')
    user.user_permissions.add(delete_permission)

    response = delete_project(client, public_project)

    assert response.status_code == HTTP_204_NO_CONTENT


def test_user_without_permission_cannot_delete_projects(client, public_project):
    response = delete_project(client, public_project)

    assert response.status_code == HTTP_403_FORBIDDEN


def test_anonymous_user_cannot_delete_projects(anonymous_client, public_project):
    response = delete_project(anonymous_client, public_project)

    assert response.status_code == HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_service_function_was_called(mocker, client, user, project):
    mocker.spy(services, 'delete_project')
    delete_permission = Permission.objects.get(codename='delete_project')
    user.user_permissions.add(delete_permission)

    delete_project(client, project)

    services.delete_project.assert_called_once()


def delete_project(client, project):
    return client.delete(reverse('project-detail', kwargs=dict(pk=project.pk)))

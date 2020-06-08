import pytest

from rest_framework.reverse import reverse
from rest_framework.status import HTTP_200_OK, HTTP_403_FORBIDDEN

from django.contrib.auth.models import Permission

from huscy.projects.models import Project

pytestmark = pytest.mark.django_db


def test_admin_user_can_view_all_projects(admin_client, projects):
    response = list_projects(admin_client)

    assert response.status_code == HTTP_200_OK
    assert_get_all_projects(response)


def test_user_with_permission_can_view_private_projects(client, user, projects):
    can_view_private_projects = Permission.objects.get(codename='can_view_private_projects')
    user.user_permissions.add(can_view_private_projects)

    response = list_projects(client)

    assert response.status_code == HTTP_200_OK
    assert_get_all_projects(response)


def test_user_without_permission_can_only_view_public_projects(client, projects):
    response = list_projects(client)

    assert response.status_code == HTTP_200_OK
    assert_get_only_public_projects(response)


def test_anonymous_user_cannot_view_projects(anonymous_client, projects):
    response = list_projects(anonymous_client)

    assert response.status_code == HTTP_403_FORBIDDEN


def list_projects(client):
    return client.get(reverse('project-list'))


def retrieve_project(client, project):
    return client.get(reverse('project-detail', kwargs=dict(pk=project.pk)))


def assert_get_all_projects(response):
    assert len(response.json()) == 10


def assert_get_only_public_projects(response):
    public = Project.VISIBILITY.get_value('public')

    assert len(response.json()) == 5
    assert all([project['visibility'] == public for project in response.json()])

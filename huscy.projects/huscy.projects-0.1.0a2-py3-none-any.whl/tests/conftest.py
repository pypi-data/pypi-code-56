from datetime import timedelta

import pytest
from model_bakery import baker

from rest_framework.test import APIClient

from huscy.projects.models import Project


ONE_HOUR = timedelta(hours=1)


@pytest.fixture
def user(django_user_model):
    return django_user_model.objects.create_user(username='user', password='password',
                                                 first_name='Phil', last_name='Stift')


@pytest.fixture
def admin_client(admin_user):
    client = APIClient()
    client.login(username=admin_user.username, password='password')
    return client


@pytest.fixture
def client(user):
    client = APIClient()
    client.login(username=user.username, password='password')
    return client


@pytest.fixture
def anonymous_client():
    return APIClient()


@pytest.fixture
def research_unit(user):
    return baker.make(
        'projects.ResearchUnit',
        name='research_unit_1',
        code='RU1',
        principal_investigator=user,
    )


@pytest.fixture
def project(public_project):
    return public_project


@pytest.fixture
def public_project():
    public = Project.VISIBILITY.get_value('public')
    return baker.make(Project, title='project_title', visibility=public)


@pytest.fixture
def public_projects():
    """ creates 5 public projects """
    public = Project.VISIBILITY.get_value('public')
    return baker.make(Project, visibility=public, _quantity=5)


@pytest.fixture
def private_projects():
    """ creates 5 private projects """
    private = Project.VISIBILITY.get_value('private')
    return baker.make(Project, visibility=private, _quantity=5)


@pytest.fixture
def projects(public_projects, private_projects):
    """ creates 5 public and 5 private projects """
    return public_projects + private_projects


@pytest.fixture
def experiment(public_project):
    return baker.make('projects.Experiment', project=public_project, description='description')


@pytest.fixture
def session(experiment):
    return baker.make(
        'projects.Session',
        experiment=experiment,
        duration=ONE_HOUR,
    )


@pytest.fixture
def data_acquisition_method(session):
    return baker.make('projects.DataAcquisitionMethod', session=session)

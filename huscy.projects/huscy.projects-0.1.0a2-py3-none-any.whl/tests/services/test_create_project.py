from model_bakery import baker

from huscy.projects import models, services

public = models.Project.VISIBILITY.get_value('public')


def test_create_project_with_creator_as_principal_investigator(user, research_unit):
    project = services.create_project('title', research_unit, user, user, public)

    assert models.Project.objects.exists()
    assert project.description == ''


def test_create_project_with_creator_not_as_principal_investigator(django_user_model, user,
                                                                   research_unit):
    principal_investigator = baker.make(django_user_model)
    project = services.create_project('title', research_unit, principal_investigator,
                                      user, public)

    assert models.Project.objects.exists()
    assert project.description == ''


def test_create_project_with_optional_description(user, research_unit):
    project = services.create_project('title', research_unit, user, user, public,
                                      description='description')

    assert models.Project.objects.exists()
    assert not project.description == ''


def test_create_project_with_optional_local_id(user, research_unit):
    project = services.create_project('title', research_unit, user, user, public,
                                      local_id=166)
    assert models.Project.objects.exists()
    assert project.local_id == 166

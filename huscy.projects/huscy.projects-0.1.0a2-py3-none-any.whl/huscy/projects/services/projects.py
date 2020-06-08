import logging

from huscy.projects.models import Project

logger = logging.getLogger('projects')


def create_project(title, research_unit, principal_investigator, creator, visibility,
                   local_id=None, description=''):
    if local_id is None:
        local_id = Project.objects.get_next_local_id(research_unit)

    project = Project.objects.create(
        description=description,
        local_id=local_id,
        principal_investigator=principal_investigator,
        research_unit=research_unit,
        title=title,
        visibility=visibility
    )
    logger.info('Project id:%d, local_id_name:%s, title:%s reserch_unit:%s has been created',
                project.id, project.local_id_name, project.title, project.research_unit.name)

    return project


def delete_project(project):
    project.delete()
    logger.info('Project id:%d, local_id_name:%s, title:%s research_unit:%s has been deleted',
                project.id, project.local_id_name, project.title, project.research_unit.name)


def get_projects(user):
    queryset = Project.objects

    if not user.has_perm('projects.can_view_private_projects'):
        public = Project.VISIBILITY.get_value('public')
        queryset = queryset.filter(visibility=public)

    return queryset.all()

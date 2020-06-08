import logging

from rest_framework import mixins, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import DjangoModelPermissions, IsAuthenticated
from rest_framework.response import Response

from huscy.projects import helpers, permissions, serializer, services

logger = logging.getLogger('projects')


class DataAcquisitionMethodViewSet(mixins.CreateModelMixin, mixins.DestroyModelMixin,
                                   mixins.UpdateModelMixin, viewsets.GenericViewSet):
    queryset = services.get_data_acquisition_methods()
    serializer_class = serializer.DataAcquisitionMethodSerializer
    permission_classes = (IsAuthenticated, )


class ExperimentViewSet(mixins.CreateModelMixin, mixins.DestroyModelMixin, mixins.UpdateModelMixin,
                        viewsets.GenericViewSet):
    queryset = services.get_experiments()
    serializer_class = serializer.ExperimentSerializer
    permission_classes = (IsAuthenticated, )


class ProjectViewSet(mixins.CreateModelMixin, mixins.DestroyModelMixin, mixins.ListModelMixin,
                     mixins.UpdateModelMixin, viewsets.GenericViewSet):
    serializer_class = serializer.ProjectSerializer
    permission_classes = (IsAuthenticated, DjangoModelPermissions | permissions.AllowAnyToCreate)

    def get_queryset(self):
        return services.get_projects(self.request.user)

    def destroy(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        logger.info('User %s from ip %s requested deletion of project with id:%d',
                    request.user.username, helpers.get_client_ip(request), pk)
        return super().destroy(request, args, kwargs)

    def perform_destroy(self, project):
        services.delete_project(project)

    @action(detail=True, methods=['get'])
    def dataacquisitionmethods(self, request, pk=None):
        methods = services.get_data_acquisition_methods(self.get_object())
        return Response(data=serializer.DataAcquisitionMethodSerializer(methods, many=True).data)

    @action(detail=True, methods=['get'])
    def experiments(self, request, pk=None):
        experiments = services.get_experiments(self.get_object())
        return Response(data=serializer.ExperimentSerializer(experiments, many=True).data)


class ResearchUnitViewSet(viewsets.ModelViewSet):
    permission_classes = (DjangoModelPermissions, )
    queryset = services.get_research_units()
    serializer_class = serializer.ResearchUnitSerializer


class SessionViewSet(viewsets.ModelViewSet):
    queryset = services.get_sessions()
    serializer_class = serializer.SessionSerializer
    permission_classes = (IsAuthenticated, )

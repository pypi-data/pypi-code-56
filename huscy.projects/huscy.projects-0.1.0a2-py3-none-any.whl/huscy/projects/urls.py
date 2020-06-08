from rest_framework.routers import DefaultRouter

from huscy.projects import views


router = DefaultRouter()
router.register('dataacquisitionmethods', views.DataAcquisitionMethodViewSet)
router.register('experiments', views.ExperimentViewSet)
router.register('projects', views.ProjectViewSet, basename='project')
router.register('researchunits', views.ResearchUnitViewSet)
router.register('sessions', views.SessionViewSet)

urlpatterns = router.urls

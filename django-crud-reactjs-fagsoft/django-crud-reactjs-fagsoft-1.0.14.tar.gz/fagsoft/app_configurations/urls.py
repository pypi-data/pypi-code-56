from rest_framework import routers
from fagsoft.app_configurations.views import AppConfiguracionViewSet, AppGeneralInfoConfigurationViewSet

router = routers.DefaultRouter()
router.register('app_configuration', AppConfiguracionViewSet, basename='configuracion')
router.register('app_configuration_general_info', AppGeneralInfoConfigurationViewSet)

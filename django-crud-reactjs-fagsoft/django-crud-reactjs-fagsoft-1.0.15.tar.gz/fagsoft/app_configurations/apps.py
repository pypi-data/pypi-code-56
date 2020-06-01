from django.apps import AppConfig


class AppConfigurationsConfig(AppConfig):
    name = 'fagsoft.app_configurations'

    def ready(self):
        import fagsoft.app_configurations.signals

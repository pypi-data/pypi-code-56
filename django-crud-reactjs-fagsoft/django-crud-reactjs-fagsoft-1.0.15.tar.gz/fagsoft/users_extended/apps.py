from django.apps import AppConfig


class UsersExtendedConfig(AppConfig):
    name = 'fagsoft.users_extended'

    def ready(self):
        import fagsoft.users_extended.signals

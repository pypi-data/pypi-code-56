from django.apps import AppConfig


class NoctonConfig(AppConfig):
    name = 'nocton'

    def ready(self, *args, **kwargs):
        from nocton.setup import watch_folders

        watch_folders()
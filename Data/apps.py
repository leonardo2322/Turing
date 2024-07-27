from django.apps import AppConfig


class DataConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Data'

    def ready(self):
        import Data.signals 
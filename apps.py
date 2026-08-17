from django.apps import AppConfig


class SignalsDemoConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'signals_demo'

    def ready(self):
        # Importing the module registers the @receiver-decorated
        # handler with Django's signal dispatcher.
        import signals_demo.signals  # noqa: F401

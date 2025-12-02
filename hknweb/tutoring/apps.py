from django.apps import AppConfig


class TutoringConfig(AppConfig):
    name = "hknweb.tutoring"

    def ready(self):
        from . import signals

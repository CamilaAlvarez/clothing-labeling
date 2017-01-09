from __future__ import unicode_literals

from django.apps import AppConfig


class LabelingAppRestConfig(AppConfig):
    name = 'labeling_app_rest'

    def ready(self):
        import labeling_app_rest.signals
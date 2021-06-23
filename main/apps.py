from django.apps import AppConfig
from django.db.models.signals import post_save


class MainConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'main'
    verbose_name = 'Главное приложение'

    def ready(self):
        # importing model classes
        from . import signals  # Ссылается на модель
        from django.contrib.auth.models import User

        # registering signals
        post_save.connect(signals.student_register, sender=User, dispatch_uid='once')

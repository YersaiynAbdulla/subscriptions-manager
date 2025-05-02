from django.apps import AppConfig
from django.db.utils import OperationalError, ProgrammingError

class SubscriptionsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "subscriptions"

    def ready(self):
        try:
            from . import category_initializer
            category_initializer.create_default_categories()
        except (OperationalError, ProgrammingError):
            # Таблицы ещё не созданы — безопасно пропустить
            pass

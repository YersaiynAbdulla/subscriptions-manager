from django.apps import AppConfig

class SubscriptionsConfig(AppConfig):
    name = 'subscriptions'

    def ready(self):
        # category_initializer.create_default_categories()
        # import subscriptions.signals  
        pass
from django.apps import apps
from django.db.models.signals import post_migrate
from django.dispatch import receiver

@receiver(post_migrate)
def create_default_categories(sender, **kwargs):
    if sender.name != "subscriptions":
        return
    Category = apps.get_model("subscriptions", "Category")
    for name in ["Netflix", "YouTube Premium", "Spotify", "others…"]:
        Category.objects.get_or_create(name=name)

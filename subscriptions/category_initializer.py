def create_default_categories():
    from .models import Category
    default_categories = ['Развлечения', 'Образование', 'Утилиты', 'Работа', 'Прочее']
    for name in default_categories:
        Category.objects.get_or_create(name=name)

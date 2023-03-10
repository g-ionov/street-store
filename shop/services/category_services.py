from shop import models


def get_categories():
    """ Получение всех категорий """
    return models.Category.objects.all()

from shop import models


def get_brands():
    """ Получение всех брендов """
    return models.Brand.objects.all()

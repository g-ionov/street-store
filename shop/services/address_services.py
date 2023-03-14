from shop import models


def get_address_if_exist_or_create(**kwargs):
    """ Получение адреса или создание нового """
    address = models.Address.objects.filter(**kwargs)
    if address.exists():
        return address.first()
    else:
        return models.Address.objects.create(**kwargs)

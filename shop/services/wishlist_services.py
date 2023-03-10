from shop import models


def get_products_in_wishlist(user):
    """ Получение товаров в избранном пользователя
    :return: Wishlist objects"""
    return models.Wishlist.objects.filter(user=user)


def is_model_in_wishlist(user, model):
    """ Проверка наличия товара в избранном """
    return models.Wishlist.objects.filter(user=user, model=model).exists()


def add_to_wishlist(user, model):
    """ Добавление товара в избранное """
    if not is_model_in_wishlist(user, model):
        models.Wishlist.objects.create(user=user, model=model)


def remove_from_wishlist(user, model):
    """ Удаление товара из избранного """
    if is_model_in_wishlist(user, model):
        models.Wishlist.objects.filter(user=user, model=model).delete()
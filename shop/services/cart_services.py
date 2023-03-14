from django.db.models import Sum, F

from shop import models


def get_models_in_cart(user):
    """ Получение товаров в корзине пользователя """
    return models.Cart.objects.filter(user=user)


def get_total_price_in_cart(user):
    """ Получение общей стоимости товаров в корзине пользователя """
    query = models.Cart.objects.filter(user=user).aggregate(
        total_price=Sum(F('model__price') * F('quantity'))).get('total_price')
    return query if query else 0


def get_total_quantity_in_cart(user):
    """ Получение общего количества товаров в корзине пользователя """
    query = models.Cart.objects.filter(user=user).aggregate(Sum('quantity')).get('quantity__sum')
    return query if query else 0


def add_to_cart(user, model, size, quantity):
    """ Добавление товара в корзину """
    if models.Cart.objects.filter(user=user, model_id=model, size=size).exists():
        models.Cart.objects.filter(user=user, model_id=model, size=size).update(quantity=quantity)
    else:
        models.Cart.objects.create(user=user, model_id=model, size=size, quantity=quantity)


def remove_from_cart(user, model):
    """ Удаление товара из корзины """
    models.Cart.objects.filter(user=user, model=model).delete()


def clear_cart(user):
    """ Очистка корзины """
    models.Cart.objects.filter(user=user).delete()

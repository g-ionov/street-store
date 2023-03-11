from django.db.models import Count

from shop import models


def get_orders_of_model(user, model):
    """ Получение заказов, содержащих товар """
    return models.Order.objects.filter(user=user, modelorder__model=model)


def get_model_sells(model):
    """ Получение количества продаж товара """
    return models.ModelOrder.objects.filter(model=model).count()


def get_best_selling_models(gender: str = None):
    """ Получение самых продаваемых товаров """
    query = models.ModelOrder.objects.values('model').annotate(Count('model')).order_by('-model__count') if not gender \
        else models.ModelOrder.objects.filter(model__gender=gender).values('model').annotate(Count('model')). \
        order_by('-model__count')
    return [models.Model.objects.get(pk=obj.get('model')) for obj in query]


def get_user_orders(user):
    """ Получение заказов пользователя """
    return models.Order.objects.filter(user=user).order_by('-created_at')


def get_models_in_order(order):
    """ Получение товаров в заказе """
    return models.ModelOrder.objects.filter(order=order)

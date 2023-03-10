from django.db.models import Sum, Q

from shop import models


def get_total_model_quantity(model):
    """ Подсчёт количества товара на складе """
    return models.Stock.objects.filter(model=model).aggregate(Sum('quantity')).get('quantity__sum')


def update_availability(model):
    """ Обновление доступности товара """
    if get_total_model_quantity(model) == 0 and model.available:
        model.available = False
        model.save()
    elif get_total_model_quantity(model) > 0 and not model.available:
        model.available = True
        model.save()


def get_similar_models(model, max_quantity):
    """ Похожие товары """
    return models.Model.objects.filter(category=model.category, brand=model.brand).filter(~Q(id=model.pk))[
           :max_quantity]


def get_model_image(model):
    """ Получение основного изображения модели"""
    return model.modelimages_set.get(main=True)


def get_new_models(gender: str = None):
    """ Получение новых товаров """
    return models.Model.objects.filter(gender=gender).order_by('-created_at')[:8] if gender else \
        models.Model.objects.order_by('-created_at')[:8]


def get_models_by_brand(brand):
    """ Получение товаров по бренду """
    return models.Model.objects.filter(brand=brand)


def get_model(model_id):
    """ Получение товара по id """
    return models.Model.objects.get(pk=model_id)

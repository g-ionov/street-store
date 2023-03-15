from django.db.models import Sum

from shop import models
from shop.services.model_services import get_total_model_quantity


def get_sizes_of_model(model):
    """ Получение размеров товара"""
    if get_total_model_quantity(model) != 0:
        query = models.Stock.objects.filter(model=model).values('size').annotate(Sum('quantity'))
        return [(models.Size.objects.get(pk=obj.get('size')),
                 obj.get('quantity__sum')) for obj in query if obj.get('quantity__sum') != 0]


def get_model_sizes_quantity_in_stock(model, size):
    """ Получение количества моделей конкретного размера на складе """
    return models.Stock.objects.filter(model=model, size=size).aggregate(Sum('quantity')).get('quantity__sum')

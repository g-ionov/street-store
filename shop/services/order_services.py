from django.db.models import Count

from shop import models
from shop.services.address_services import get_address_if_exist_or_create
from shop.services.cart_services import clear_cart, get_models_in_cart, get_total_price_in_cart
from shop.services.coupon_services import get_total_price_in_cart_with_coupon, check_using_possibility
from shop.services.user_services import get_recipient_if_exist_or_create


def get_orders_of_model(user, model):
    """ Получение заказов, содержащих товар """
    return models.Order.objects.filter(user=user, modelorder__model=model).distinct()


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


def create_order(**kwargs):
    """ Создание заказа """
    user = kwargs.get('user')
    recipient = get_recipient_if_exist_or_create(first_name=kwargs['first_name'],
                                                 last_name=kwargs['last_name'],
                                                 phone=kwargs['phone']) \
        if all(map(lambda x: kwargs.get(x) != '', ('first_name', 'last_name', 'phone'))) else None

    is_user_recipient = False if recipient else True

    if kwargs.get('coupon') != '' and check_using_possibility(kwargs.get('coupon'), user):
        coupon = kwargs.get('coupon')
        price = get_total_price_in_cart_with_coupon(user, kwargs.get('coupon'))
    else:
        price = get_total_price_in_cart(user)
        coupon = None

    for key in ('user', 'first_name', 'last_name', 'phone', 'coupon'): kwargs.pop(key)
    address = get_address_if_exist_or_create(**kwargs)
    order = models.Order.objects.create \
        (user=user, recipient=recipient, address=address, is_user_recipient=is_user_recipient, price=price,
         coupon=coupon)
    for model in get_models_in_cart(user):
        models.ModelOrder.objects.create(order=order, model=model.model, size=model.size, quantity=model.quantity)
    clear_cart(user)
    return order

import datetime

from django.db.models import Sum

from shop import models


def check_period(start_date, end_date):
    """ Проверка корректности даты начала и даты окончания периода """
    if start_date > end_date or start_date > datetime.date.today() or end_date > datetime.date.today():
        return False
    return True


def get_total_orders_quantity(start_date=None, end_date=None):
    """ Подсчёт количества заказов за определенный период """
    if start_date and end_date:
        return models.Order.objects.filter(created_at__range=[start_date, end_date]).count()
    else:
        return models.Order.objects.count()


def get_total_orders_sum(start_date=None, end_date=None):
    """ Подсчёт суммы заказов за определенный период """
    if start_date and end_date:
        return models.Order.objects.filter(created_at__range=[start_date, end_date]).aggregate(Sum('price')).get(
            'price__sum')
    else:
        return models.Order.objects.aggregate(Sum('price')).get('price__sum')


def get_total_users_quantity(start_date=None, end_date=None):
    """ Подсчёт количества пользователей за определенный период """
    if start_date and end_date:
        return models.User.objects.filter(date_joined__range=[start_date, end_date]).count()
    else:
        return models.User.objects.count()


def get_average_order_sum(start_date=None, end_date=None):
    """ Подсчёт средней суммы заказа с округлением до сотых """
    if get_total_orders_quantity(start_date, end_date) == 0:
        return 0
    else:
        return round(get_total_orders_sum(start_date, end_date) / get_total_orders_quantity(start_date, end_date), 2)


def get_statistic(start_date=None, end_date=None):
    """ Получение статистики """
    return {
        'total_orders_quantity': get_total_orders_quantity(start_date, end_date),
        'total_orders_sum': get_total_orders_sum(start_date, end_date),
        'total_users_quantity': get_total_users_quantity(start_date, end_date),
        'average_order_sum': get_average_order_sum(start_date, end_date),
    }


def check_permission_for_statistic(user):
    """ Проверка прав доступа к статистике """
    return user.is_superuser or user.is_staff

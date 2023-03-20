import datetime

from shop import models
from shop.services.cart_services import get_total_price_in_cart


def get_coupon_users(coupon):
    """ Получение пользователей купона """
    return coupon.users.all()


def get_coupon_uses_by_user(coupon, user):
    """ Получение количества использований купона пользователем """
    return models.Order.objects.filter(coupon=coupon, user=user).count()


def check_using_possibility(code, user=None):
    """ Проверка возможности использования купона """

    # Проверка работоспособности купона без привязки к пользователю
    if models.Coupon.objects.filter(code=code).count() == 0:
        return False
    else:
        coupon = models.Coupon.objects.get(code=code)
    if not coupon.is_active:
        return False
    if coupon.expiration_date < datetime.date.today():
        return False
    if not coupon.max_uses.is_infinite and coupon.max_uses.max_uses <= coupon.times_used:
        return False

    # Проверка возможности использования купона пользователем
    if user:
        if not coupon.all_users and user not in get_coupon_users(coupon):
            return False
        if get_coupon_uses_by_user(coupon, user) >= coupon.max_uses.uses_per_user:
            return False
    return True


def get_total_price_in_cart_with_coupon(user, code):
    """ Получение стоимости корзины с купоном"""
    return get_total_price_in_cart(user) * models.Coupon.objects.get(code=code).discount / 100

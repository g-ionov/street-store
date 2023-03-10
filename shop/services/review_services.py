from django.db.models import Avg

from shop import models


def get_total_reviews_quantity(model):
    """ Подсчёт количества отзывов о товаре """
    return models.Review.objects.filter(model=model).count()


def get_average_rating(model):
    """ Подсчёт среднего рейтинга товара с округлением до сотых"""
    if get_total_reviews_quantity(model) == 0:
        return 0
    else:
        return round(models.Review.objects.filter(model=model).aggregate(Avg('grade')).get('grade__avg'), 2)


def is_review_exists(order, user, model):
    """ Проверка наличия отзыва о товаре от пользователя """
    return models.Review.objects.filter(order=order, user=user, model=model).exists()


def create_or_update_review(user, model, order, grade, text):
    """ Создание отзыва """
    if is_review_exists(order, user, model):
        models.Review.objects.filter(order=order, user=user, model=model).update(grade=grade, text=text)
    else:
        models.Review.objects.create(user=user, model=model, order=order, grade=grade, text=text)


def delete_review(review_id):
    """ Удаление отзыва """
    models.Review.objects.filter(pk=review_id).delete()
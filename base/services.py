import random
import string

from django.utils.safestring import mark_safe
from config import settings


def get_item_number_length(length=5):
    """ Длина артикула """
    return settings.ITEM_NUMBER_LENGTH if hasattr(settings, 'ITEM_NUMBER_LENGTH') else length


def get_random_code(length=12):
    """ Генерация случайного кода купона"""
    length = settings.COUPON_CODE_LENGTH if hasattr(settings, 'COUPON_CODE_LENGTH') else length
    return ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(length))


def get_random_item_number(length=5):
    """ Генерация случайного артикула"""
    length = get_item_number_length(length)
    return ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(length))


def get_image_html(img_name, width=50):
    """ Вывод изображения в админке """
    photo = img_name
    if photo:
        return mark_safe(f"<img src='{photo.url}' width={width}>")


def get_grades(step=0.25):
    """ Генерация списка оценок товара с указанным шагом """
    if step not in (0.05, 0.1, 0.2, 0.25, 0.5, 1):
        raise ValueError('Step must be in (0.05, 0.1, 0.2, 0.25, 0.5, 1)')

    grades = [(i * step, i * step) for i in range(int(5 / step + 1))]

    return grades


def get_grades_for_template(grades):
    """ Создание оценок для выпадающего списка при формировании отзыва """
    return [grade[0] for grade in grades]


def get_image_path_upload(instance, file):
    """ Построение пути к файлу в формате: (media)/model/name/photo (для дополнительных фото модели)"""
    return f'model/{instance.model.name}/{instance.model.item_number}/{file}'

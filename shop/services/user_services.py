from shop import models


def edit_user(user, data):
    """ Редактирование пользователя """
    models.User.objects.filter(pk=user.pk).update(**data)


def delete_user(user):
    """ Удаление пользователя """
    models.User.objects.filter(pk=user.pk).delete()
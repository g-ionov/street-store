from shop import models


def edit_user(user, data):
    """ Редактирование пользователя """
    models.User.objects.filter(pk=user.pk).update(**data)


def delete_user(user):
    """ Удаление пользователя """
    models.User.objects.filter(pk=user.pk).delete()


def get_recipient_if_exist_or_create(**kwargs):
    """ Получение получателя или создание нового """
    recipient = models.Recipient.objects.filter(**kwargs)
    if recipient.exists():
        return recipient.first()
    else:
        return models.Recipient.objects.create(**kwargs)

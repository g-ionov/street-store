from django.db.models import Sum, Avg, Q, Count, F
import shop.models as models  # Данный модуль импортируется для избежания циклического импорта


def get_total_model_quantity(model):
    """ Подсчёт количества товара на складе """
    return models.Stock.objects.filter(model=model).aggregate(Sum('quantity')).get('quantity__sum')


def get_orders_of_model(user, model):
    """ Получение заказов, содержащих товар """
    return models.Order.objects.filter(user=user, modelorder__model=model)


def update_availability(model):
    """ Обновление доступности товара """
    if get_total_model_quantity(model) == 0 and model.available:
        model.available = False
        model.save()
    elif get_total_model_quantity(model) > 0 and not model.available:
        model.available = True
        model.save()


def get_sizes_of_model(model):
    """ Получение размеров товара"""
    if get_total_model_quantity(model) != 0:
        query = models.Stock.objects.filter(model=model).values('size').annotate(Sum('quantity'))
        return [(models.Size.objects.get(pk=obj.get('size')),
                 obj.get('quantity__sum')) for obj in query if obj.get('quantity__sum') != 0]


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


def get_similar_products(model, max_quantity):
    """ Похожие товары """
    return models.Model.objects.filter(category=model.category, brand=model.brand).filter(~Q(id=model.pk))[
           :max_quantity]


def get_model_image(self):
    """ Получение основного изображения модели"""
    return self.modelimages_set.get(main=True)


def get_products_in_wishlist(user):
    """ Получение товаров в избранном пользователя
    :return: Wishlist objects"""
    return models.Wishlist.objects.filter(user=user)


def get_categories():
    """ Получение всех категорий """
    return models.Category.objects.all()


def is_model_in_wishlist(user, model):
    """ Проверка наличия товара в избранном """
    return models.Wishlist.objects.filter(user=user, model=model).exists()


def add_to_wishlist(user, model):
    """ Добавление товара в избранное """
    if is_model_in_wishlist(user, model):
        return False
    else:
        models.Wishlist.objects.create(user=user, model=model)
        return True


def remove_from_wishlist(user, model):
    """ Удаление товара из избранного """
    if is_model_in_wishlist(user, model):
        models.Wishlist.objects.filter(user=user, model=model).delete()
        return True
    else:
        return False


def get_model_sells(model):
    """ Получение количества продаж товара """
    return models.ModelOrder.objects.filter(model=model).count()


def get_new_models(gender: str = None):
    """ Получение новых товаров """
    return models.Model.objects.filter(gender=gender).order_by('-created_at')[:8] if gender else \
        models.Model.objects.order_by('-created_at')[:8]


def get_best_selling_products(gender: str = None):
    """ Получение самых продаваемых товаров """
    query = models.ModelOrder.objects.values('model').annotate(Count('model')).order_by('-model__count') if not gender \
        else models.ModelOrder.objects.filter(model__gender=gender).values('model').annotate(Count('model')). \
        order_by('-model__count')
    return [models.Model.objects.get(pk=obj.get('model')) for obj in query]


def get_brands():
    """ Получение всех брендов """
    return models.Brand.objects.all()


def get_models_by_brand(brand):
    """ Получение товаров по бренду """
    return models.Model.objects.filter(brand=brand)


def get_products_in_cart(user):
    """ Получение товаров в корзине пользователя """
    return models.Cart.objects.filter(user=user)


def get_total_price_in_cart(user):
    """ Получение общей стоимости товаров в корзине пользователя """
    query = models.Cart.objects.filter(user=user).aggregate(
        total_price=Sum(F('model__price') * F('quantity'))).get('total_price')
    return query if query else 0


def get_total_quantity_in_cart(user):
    """ Получение общего количества товаров в корзине пользователя """
    query = models.Cart.objects.filter(user=user).aggregate(Sum('quantity')).get('quantity__sum')
    return query if query else 0


def get_model(model_id):
    """ Получение товара по id """
    return models.Model.objects.get(pk=model_id)


def add_to_cart(user, model, size, quantity):
    """ Добавление товара в корзину """
    if models.Cart.objects.filter(user=user, model_id=model, size=size).exists():
        models.Cart.objects.filter(user=user, model_id=model, size=size).update(quantity=quantity)
    else:
        models.Cart.objects.create(user=user, model_id=model, size=size, quantity=quantity)


def remove_from_cart(user, model):
    """ Удаление товара из корзины """
    models.Cart.objects.filter(user=user, model=model).delete()


def get_models_by_category(category: int = None, gender: str = None):
    """ Получение товаров по категории """
    if category and gender:
        return models.Model.objects.filter(category=category, gender=gender)
    elif category:
        return models.Model.objects.filter(category=category)
    elif gender:
        return models.Model.objects.filter(gender=gender)
    else:
        return models.Model.objects.all()


def get_model_sizes_quantity_in_stock(model, size):
    """ Получение количества моделей конкретного размера на складе """
    return models.Stock.objects.filter(model=model, size=size).aggregate(Sum('quantity')).get('quantity__sum')


def delete_user(user):
    """ Удаление пользователя """
    models.User.objects.filter(pk=user.pk).delete()


def edit_user(user, data):
    """ Редактирование пользователя """
    models.User.objects.filter(pk=user.pk).update(**data)

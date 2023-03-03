from django import template

from shop.services import get_model_image, get_total_model_quantity, get_total_reviews_quantity, get_average_rating, \
    get_sizes_of_model, get_similar_products, get_categories, is_model_in_wishlist, get_products_in_cart, \
    get_total_price_in_cart, get_total_quantity_in_cart, get_products_in_wishlist, get_orders_of_model

register = template.Library()


@register.simple_tag
def main_model_image(model):
    """ Тег вывода основного изображения модели"""
    return get_model_image(model).image.url


@register.inclusion_tag('shop/include/small_item.html')
def small_item(model):
    """ Тег вывода карточки товара"""
    return {'model': model}


@register.inclusion_tag('shop/include/small_item_line.html')
def small_item_line(models):
    """ Тег вывода карточки товара"""
    return {'models': models}


@register.inclusion_tag('shop/include/products_slider_tab.html')
def products_list_line(models):
    """ Тег вывода новых моделей"""
    return {'models': models}


@register.inclusion_tag('shop/include/category_block.html')
def category_block(category_name, category_name_in_href, new_models_func, best_selling_products_func):
    """ Тег вывода категории"""
    return {'category_name': category_name,
            'category_name_in_href': category_name_in_href,
            'new_models': new_models_func,
            'best_selling_products': best_selling_products_func}


@register.inclusion_tag('shop/include/mini_cart.html')
def mini_cart(user):
    """ Тег вывода мини корзины"""
    return {'cart_item': get_products_in_cart(user), 'total_price': get_total_price_in_cart(user)}


@register.inclusion_tag('shop/include/add_to_wishlist_button.html')
def add_to_wishlist_button(model):
    """ Тег вывода кнопки добавления товара в избранное"""
    return {'model': model}


register.simple_tag(func=get_total_model_quantity, name="total_model_quantity")
register.simple_tag(func=get_total_reviews_quantity, name="reviews_quantity")
register.simple_tag(func=get_average_rating, name="average_rating")
register.simple_tag(func=get_sizes_of_model, name="model_sizes")
register.simple_tag(func=get_similar_products, name="get_similar_products")
register.simple_tag(func=get_categories, name="categories")
register.simple_tag(func=is_model_in_wishlist, name="model_in_wishlist")
register.simple_tag(func=get_total_price_in_cart, name="total_price_in_cart")
register.simple_tag(func=get_total_quantity_in_cart, name="total_quantity_in_cart")
register.simple_tag(func=get_products_in_wishlist, name="products_in_wishlist")
register.simple_tag(func=get_products_in_cart, name="products_in_cart")
register.simple_tag(func=get_orders_of_model, name="orders_of_model")

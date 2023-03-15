from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from django.utils.text import slugify
from phonenumber_field.modelfields import PhoneNumberField
from base.services import get_random_code, get_grades, get_image_path_upload, get_item_number_length, \
    get_random_item_number
from mptt.models import MPTTModel, TreeForeignKey

from shop import services

GENDERS = [('M', 'Male'), ('F', 'Female')]


class User(AbstractUser):
    """ Пользователь """
    birth_date = models.DateField('Дата рождения', null=True, blank=True)
    phone = PhoneNumberField(verbose_name='Номер телефона', region='RU', unique=True)
    email = models.EmailField(verbose_name='Адрес электронной почты', unique=True)

    def __str__(self):
        return self.username


class Recipient(models.Model):
    """ Получатель """
    first_name = models.CharField(verbose_name='Имя', max_length=64)
    last_name = models.CharField(verbose_name='Фамилия', max_length=64)
    phone = PhoneNumberField(verbose_name='Номер телефона', region='RU')

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    class Meta:
        verbose_name = 'Получатель'
        verbose_name_plural = 'Получатели'
        ordering = ['last_name']


class Address(models.Model):
    """ Адрес заказа """
    city = models.CharField(verbose_name='Город', max_length=25)
    street = models.CharField(verbose_name='Улица', max_length=32)
    number = models.CharField(verbose_name='Дом', max_length=4)
    block = models.CharField(verbose_name='Корпус', max_length=3, null=True, blank=True)
    apartment = models.CharField(verbose_name='Квартира', max_length=6, null=True, blank=True)
    zip_code = models.CharField(verbose_name='Индекс', max_length=6)

    def __str__(self):
        return f'г. {self.city} ул. {self.street} д. {self.number} - {self.zip_code}'

    class Meta:
        verbose_name = 'Адрес заказа'
        verbose_name_plural = 'Адреса заказа'
        ordering = ['city']


class Order(models.Model):
    """ Заказ """
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Заказчик')
    address = models.ForeignKey(Address, on_delete=models.SET_NULL, verbose_name='Адрес', blank=True, null=True)
    is_user_recipient = models.BooleanField(verbose_name='Пользователь - получатель', default=True)
    created_at = models.DateTimeField(verbose_name='Создан', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='Обновлен', auto_now=True)
    recipient = models.ForeignKey(Recipient, verbose_name='Получатель', blank=True, on_delete=models.SET_NULL,
                                  null=True)
    paid = models.BooleanField(verbose_name='Оплачен', default=False)
    price = models.DecimalField(verbose_name='Стоимость', max_digits=8, decimal_places=2)

    def __str__(self):
        return f'Заказ {self.pk} пользователя {self.user}'

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        ordering = ['-created_at']


class Category(MPTTModel):
    """ Категория товара """
    name = models.CharField(verbose_name='Название', max_length=20)
    url = models.SlugField(max_length=160, unique=True)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    def __str__(self):
        return self.name

    class MPTTMeta:
        order_insertion_by = ['name']

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Size(models.Model):
    """ Размер модели товара """
    UK_US = [(f'{3 + x * 0.5}', f'{3 + x * 0.5}') for x in range(23)] + \
            [('XS', 'XS'), ('S', 'S'), ('M', 'M'), ('L', 'L'), ('XL', 'XL'), ('2XL', '2XL'), ('3XL', '3XL')]
    RU_SIZES = [(f'{35 + x}', f'{35 + x}') for x in range(26)]
    JP_SIZES = [(f'{21 + x * 0.5}', f'{21 + x * 0.5}') for x in range(21)]

    category = models.ForeignKey(Category, verbose_name='Категория', on_delete=models.CASCADE)
    us = models.CharField(verbose_name='US', max_length=4, choices=UK_US)
    ru = models.CharField(verbose_name='RU', max_length=4, choices=RU_SIZES)
    uk = models.CharField(verbose_name='UK', max_length=4, choices=UK_US, null=True, blank=True)
    jp = models.CharField(verbose_name='JP', max_length=4, choices=JP_SIZES, null=True, blank=True)
    gender = models.CharField(verbose_name='Пол', default='M', choices=GENDERS, max_length=2, null=True, blank=True)

    def __str__(self):
        return f'{self.us} US {self.gender} ({self.ru} RU)'

    class Meta:
        verbose_name = 'Размер'
        verbose_name_plural = 'Размеры'
        ordering = ['category']


class Brand(models.Model):
    """ Бренд """
    name = models.CharField(verbose_name='Имя', max_length=50)
    description = models.TextField(verbose_name='Описание', blank=True)
    logo = models.ImageField(verbose_name='Логотип', upload_to='brand/')
    created_at = models.DateTimeField(verbose_name='Создан', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='Обновлен', auto_now=True)
    url = models.SlugField(max_length=160, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Бренд'
        verbose_name_plural = 'Бренды'


class Model(models.Model):
    """ Модель товара """
    item_number_length = get_item_number_length()

    category = models.ForeignKey(Category, models.CASCADE, verbose_name='Категория')
    brand = models.ForeignKey(Brand, models.CASCADE, verbose_name='Бренд')
    name = models.CharField(verbose_name='Модель', max_length=160)
    price = models.DecimalField(verbose_name='Стоимость', max_digits=8, decimal_places=2)
    available = models.BooleanField(verbose_name='Доступен', default=False)
    description = models.TextField(verbose_name='Описание', null=True, blank=True)
    country = models.CharField(verbose_name='Страна производства', max_length=64)
    sale = models.DecimalField(verbose_name='Скидка', max_digits=8, decimal_places=2, default=0)
    created_at = models.DateTimeField(verbose_name='Создан', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='Обновлен', auto_now=True)
    url = models.SlugField(max_length=160, unique=True)
    item_number = models.CharField(max_length=item_number_length, verbose_name='Артикул',
                                   default=get_random_item_number, unique=True)
    gender = models.CharField(verbose_name='Пол', default='M', choices=GENDERS, max_length=2, null=True, blank=True)

    def save(self, *args, **kwargs):
        self.url = slugify(self.name) + '-' + self.item_number.lower()
        super(Model, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('model_detail', kwargs={'slug': self.url})

    def __str__(self):
        return self.name

    def get_current_price(self):
        return self.price - self.sale

    def get_discount_percentage(self):
        return round((1 - self.get_current_price() / self.price) * 100)

    class Meta:
        verbose_name = 'Модель'
        verbose_name_plural = 'Модели'


class Stock(models.Model):
    """ Склад (поступление/убытие товара) """
    model = models.ForeignKey(Model, models.CASCADE, verbose_name='Модель', related_name='stock')
    size = models.ForeignKey(Size, models.CASCADE, verbose_name='Размер')
    date = models.DateTimeField(verbose_name='Дата', auto_now_add=True)
    quantity = models.SmallIntegerField(verbose_name='Количество')

    def __str__(self):
        return f'{self.model}: {self.quantity}'

    def save(self, *args, **kwargs):
        super(Stock, self).save(*args, **kwargs)
        services.model_services.update_availability(self.model)

    class Meta:
        verbose_name = 'Склад'


class ModelOrder(models.Model):
    """ Товары в заказе """
    order = models.ForeignKey(Order, models.SET_NULL, verbose_name='Заказ', null=True, related_name='modelorder')
    model = models.ForeignKey(Model, models.SET_NULL, verbose_name='Модель', null=True)
    quantity = models.PositiveSmallIntegerField(verbose_name='Количество')
    size = models.ForeignKey(Size, models.CASCADE, verbose_name='Размер')

    def __str__(self):
        return f'{self.order}: {self.model} ({self.size}) - {self.quantity}'

    def save(self, *args, **kwargs):
        """ Убирает товар со склада после оформления заказа """
        super(ModelOrder, self).save(*args, **kwargs)
        Stock(model=self.model, quantity=-self.quantity, size=self.size).save()

    class Meta:
        verbose_name = 'Товары в заказе'


class Cart(models.Model):
    """ Корзина """
    user = models.ForeignKey(User, models.SET_NULL, verbose_name='Пользователь', null=True)
    model = models.ForeignKey(Model, models.SET_NULL, verbose_name='Модель', null=True)
    quantity = models.PositiveSmallIntegerField(verbose_name='Количество')
    size = models.ForeignKey(Size, models.CASCADE, verbose_name='Размер')

    def __str__(self):
        return f'{self.user}: {self.model} - {self.size} ({self.quantity} шт.)'

    class Meta:
        verbose_name = 'Корзина'


class Wishlist(models.Model):
    """ Список желаемого """
    user = models.ForeignKey(User, models.SET_NULL, verbose_name='Пользователь', null=True)
    model = models.ForeignKey(Model, models.SET_NULL, verbose_name='Модель', null=True)

    def __str__(self):
        return f'{self.user}: {self.model}'

    class Meta:
        verbose_name = 'Список желаемого'


class Review(models.Model):
    """ Отзыв """
    GRADES = get_grades(0.25)

    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.SET_NULL, null=True)
    model = models.ForeignKey(Model, verbose_name='Модель', on_delete=models.CASCADE)
    order = models.ForeignKey(Order, verbose_name='Заказ', on_delete=models.SET_NULL, null=True)
    grade = models.FloatField(choices=GRADES, verbose_name='Оценка')
    text = models.TextField(verbose_name='Отзыв', null=True, blank=True)
    created_at = models.DateTimeField(verbose_name='Создан', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='Обновлен', auto_now=True)

    def __str__(self):
        return f'{self.user} - {self.grade}'

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'


class MaxUses(models.Model):
    """ Максимальное количество использований """
    max_uses = models.PositiveSmallIntegerField(verbose_name='Максимальное количество использований', default=0)
    is_infinite = models.BooleanField(verbose_name='Бесконечный', default=False)
    uses_per_user = models.IntegerField(default=1, verbose_name="Использование одним клиентом")

    def __str__(self):
        return f'Макс. исп. {self.max_uses}; Беск. {self.is_infinite}; Исп. одним польз. {self.uses_per_user}'

    class Meta:
        verbose_name = 'Максимальное количество использований'


class Coupon(models.Model):
    """ Скидочный купон """
    users = models.ManyToManyField(User, verbose_name='Пользователи, которые могут применить купон', blank=True)
    max_uses = models.ForeignKey(MaxUses, models.PROTECT, verbose_name='Максимально использований')
    discount = models.PositiveSmallIntegerField(default=0, verbose_name='Скидка %',
                                                validators=[MinValueValidator(0), MaxValueValidator(100)])
    code = models.CharField(max_length=50, default=get_random_code, unique=True, verbose_name='Код купона')
    times_used = models.PositiveIntegerField(default=0, editable=False, verbose_name="Счетчик использований")
    all_users = models.BooleanField(default=True, verbose_name="Доступен всем пользователям")
    is_active = models.BooleanField(default=True, verbose_name='Активен')
    expiration_date = models.DateField(verbose_name='Дата завершения', blank=True, null=True)
    created_at = models.DateTimeField(verbose_name='Создан', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='Обновлен', auto_now=True)

    def __str__(self):
        return f'{self.code} - {self.discount}%'

    class Meta:
        verbose_name = 'Купон'
        verbose_name_plural = 'Купоны'
        ordering = ['-discount']


class CouponUses(models.Model):
    """ Использование купона """
    user = models.ForeignKey(User, models.CASCADE, verbose_name='Пользователь')
    coupon = models.ForeignKey(Coupon, models.CASCADE, verbose_name='Купон')
    order = models.ForeignKey(Order, models.CASCADE, verbose_name='Заказ')

    def __str__(self):
        return f'{self.user} - {self.coupon}'

    class Meta:
        verbose_name = 'Использование купона'
        verbose_name_plural = 'Использование купонов'


class ModelImages(models.Model):
    """ Фотографии модели """
    model = models.ForeignKey(Model, on_delete=models.CASCADE, verbose_name='Фото модели')
    image = models.ImageField(verbose_name='Изображение', upload_to=get_image_path_upload)
    main = models.BooleanField(verbose_name='Основная', default=False)

    def __str__(self):
        return f'Фото модели {self.model}'

    class Meta:
        verbose_name = 'Фотография'
        verbose_name_plural = 'Фотографии'

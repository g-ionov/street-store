from django.contrib import admin
from base.services import get_image_html

from .models import User, Recipient, Address, Order, Category, Size, Brand, Model, Stock, ModelOrder, Cart, \
    Review, MaxUses, Coupon, ModelImages, Wishlist


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'username', 'first_name', 'last_name', 'phone', 'email', 'is_staff', 'is_active', 'is_superuser')
    search_fields = ('username', 'first_name', 'last_name', 'phone', 'email')
    list_filter = list_editable = ('is_staff', 'is_active', 'is_superuser')


@admin.register(Recipient)
class RecipientAdmin(admin.ModelAdmin):
    list_display = list_display_links = search_fields = ('first_name', 'last_name', 'phone')


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = search_fields = ('city', 'street', 'number', 'block', 'apartment', 'zip_code')
    list_display_links = ('city', 'zip_code')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'address', 'is_user_recipient', 'paid', 'created_at', 'updated_at')
    search_fields = list_display_links = ('user', 'address')
    list_filter = ('paid', 'is_user_recipient')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'url')
    prepopulated_fields = {'url': ('name',)}


@admin.register(Size)
class SizeAdmin(admin.ModelAdmin):
    list_display = ('category', 'ru', 'us', 'uk', 'jp', 'gender')
    list_filter = ('gender',)


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('name', 'get_image', 'url')
    prepopulated_fields = {'url': ('name',)}

    @staticmethod
    def get_image(obj):
        return get_image_html(obj.logo)


class ImageInline(admin.TabularInline):
    model = ModelImages
    readonly_fields = ('get_image',)
    extra = 1

    @staticmethod
    def get_image(obj):
        return get_image_html(obj.image, 300)


@admin.register(Model)
class ModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'item_number', 'price', 'category', 'brand', 'available', 'sale', 'url')
    list_display_links = ('name', 'item_number')
    list_filter = ('brand', 'available', 'sale')
    search_fields = ('name', 'item_number')
    list_editable = ('sale',)
    prepopulated_fields = {'url': ('name',)}
    inlines = [ImageInline]


@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = ('model', 'size', 'date', 'quantity')


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'model', 'grade')
    search_fields = ('user', 'model')


@admin.register(MaxUses)
class MaxUsesAdmin(admin.ModelAdmin):
    list_display = ('max_uses', 'is_infinite', 'uses_per_user')
    list_editable = list_filter = ('is_infinite',)


@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ('code', 'discount', 'times_used', 'all_users', 'is_active', 'expiration_date')
    list_editable = list_filter = ('all_users', 'is_active')
    readonly_fields = ('times_used',)


@admin.register(ModelImages)
class ModelImagesAdmin(admin.ModelAdmin):
    list_display = list_display_links = ('model', 'get_image', 'main')

    @staticmethod
    def get_image(obj):
        return get_image_html(obj.image)


admin.site.register(Cart)
admin.site.register(Wishlist)
admin.site.register(ModelOrder)

from django.urls import path

from .views import ModelDetailView, AddReview, MainView, \
    RegisterUserView, CartView, WishlistView, UserView, OrdersView

urlpatterns = [
    path('', MainView.as_view(), name='index'),
    path('me/', UserView.as_view(), name='me'),
    path('orders/', OrdersView.as_view(), name='orders'),
    path("wishlist/", WishlistView.as_view(), name="wishlist"),
    path("wishlist/<int:pk>", WishlistView.as_view(), name="add_or_remove_from_wishlist"),
    path("cart/", CartView.as_view(), name="cart"),
    path("cart/<int:pk>", CartView.as_view(), name="add_or_remove_from_cart"),
    path("model/<slug:slug>/", ModelDetailView.as_view(), name="model_detail"),
    path("review/<str:action>", AddReview.as_view(), name="review"),
    path("register/", RegisterUserView.as_view(), name="register_user"),
]

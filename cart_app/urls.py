# Carts_App/urls.py
from django.urls import path
from cart_app import views

urlpatterns = [
    path('add_to_cart/<int:card_type_id>/', views.AddToCartView.as_view(), name='add_to_cart'),
    path('cart/', views.CartView.as_view(), name='cart_view'),
    path('remove_from_cart/<int:cart_item_id>/', views.RemoveFromCartView.as_view(), name='remove_from_cart'),
    path('clear_cart/', views.ClearCartView.as_view(), name='clear_cart'),
]

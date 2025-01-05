# cart_app/models.py
from django.db import models
from django.contrib.auth.models import User
from product_app.models import CardPrice
from orders_app.models import OrderItem

class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cart', verbose_name="User associated with the cart")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Date created")

    def __str__(self):
        return f"Cart of {self.user.username}"
    
    class Meta:
        verbose_name = "Cart"
        verbose_name_plural = "Cart"

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items', verbose_name="Related cart")
    card = models.ForeignKey(CardPrice, on_delete=models.CASCADE, verbose_name="Related card")
    amount = models.PositiveIntegerField(default=1, verbose_name="Quantity")
    order_item = models.ForeignKey(OrderItem, on_delete=models.SET_NULL, related_name='cart_items', null=True, blank=True)
    
    def __str__(self):
        return f"{self.amount} x {self.card} in Cart ({self.cart.user.username})"

    class Meta:
        verbose_name = "CartItem"
        verbose_name_plural = "CartItem"

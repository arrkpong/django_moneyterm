# orders_app/models.py
from django.db import models
from django.contrib.auth.models import User
from product_app.models import CardPrice

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="User")
    total_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Total Price")
    order_date = models.DateTimeField(auto_now_add=True, verbose_name="Order Date")
    status = models.CharField(max_length=100, default='Pending', verbose_name="Status")

    def __str__(self):
        return f"Order #{self.pk} by {self.user.username}"

    class Meta:
        verbose_name = "Order"
        verbose_name_plural = "Orders"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name="Order")
    card = models.ForeignKey(CardPrice, on_delete=models.CASCADE, verbose_name="Related Card")
    amount = models.PositiveIntegerField(default=1, verbose_name="Quantity")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Price")
    serial_number = models.CharField(max_length=16, verbose_name="Serial Number", blank=True, null=True)
    pin = models.CharField(max_length=4, verbose_name="PIN", blank=True, null=True)

    def __str__(self):
        return f"{self.amount} x {self.card} in Order #{self.order.pk}"

    class Meta:
        verbose_name = "Order Item"
        verbose_name_plural = "Order Items"

class Feedback(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='feedbacks', verbose_name="Order")
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="User")
    rating = models.IntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')], verbose_name="Rating")
    comment = models.TextField(verbose_name="Comment", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")

    def __str__(self):
        return f"Feedback for Order #{self.order.pk} by {self.user.username}"

    class Meta:
        verbose_name = "Feedback"
        verbose_name_plural = "Feedback"


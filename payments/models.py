# payments/models.py
from django.db import models
from django.contrib.auth.models import User

class OrderStatus(models.Model):
    PENDING = 'pending'
    COMPLETED = 'completed'
    CANCELLED = 'cancelled'
    REFUNDED = 'refunded'

    STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (COMPLETED, 'Completed'),
        (CANCELLED, 'Cancelled'),
        (REFUNDED, 'Refunded'),
    ]

    order = models.ForeignKey('orders_app.Order', on_delete=models.CASCADE, related_name='order_statuses')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=PENDING)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.order} - {self.status}"

    class Meta:
        verbose_name = 'Order status'
        verbose_name_plural = 'Order statuses'

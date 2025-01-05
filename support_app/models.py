#support_app\models.py
from django.db import models
from django.contrib.auth.models import User

class Ticket(models.Model):
    STATUS_CHOICES = [
        ('Open', 'Open'),
        ('Closed', 'Closed'),
    ]

    customer = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Customer')
    subject = models.CharField(max_length=255, verbose_name='Subject')
    message = models.TextField(verbose_name='Message')
    image = models.ImageField(upload_to='ticket_images/', blank=True, null=True, verbose_name='Image')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Open', verbose_name='Status')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created At')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated At')

    def __str__(self):
        return f'Ticket {self.id} by {self.customer.username}'

    class Meta:
        verbose_name = 'Ticket'
        verbose_name_plural = 'Tickets'

class Response(models.Model):
    ticket = models.ForeignKey(Ticket, related_name='responses', on_delete=models.CASCADE, verbose_name='Ticket')
    responder = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Responder')
    message = models.TextField(verbose_name='Message')
    image = models.ImageField(upload_to='response_images/', blank=True, null=True, verbose_name='Image')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created At')

    def __str__(self):
        return f'Response {self.id} by {self.responder.username}'

    class Meta:
        verbose_name = 'Response'
        verbose_name_plural = 'Responses'


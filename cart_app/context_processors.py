# Carts_App/context_processors.py

from .models import Cart
from django.db.models import Sum

def cart_quantity(request):
    total_quantity = 0
    
    if request.user.is_authenticated:
        try:
            cart = request.user.cart
            total_quantity = cart.items.aggregate(total_quantity=Sum('amount'))['total_quantity'] or 0
        except Cart.DoesNotExist:
            pass
    
    return {'total_quantity': total_quantity}


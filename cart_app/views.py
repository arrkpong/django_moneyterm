#cart_app\views.py
from django.http import HttpResponseNotAllowed,HttpResponseBadRequest
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views import View
from decimal import Decimal
from cart_app.models import Cart, CartItem
from product_app.models import CardPrice, CardType
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.contrib.auth.signals import user_logged_out
from django.dispatch import receiver

class AddToCartView(LoginRequiredMixin, View):
    def post(self, request, card_type_id, *args, **kwargs):
        card_type = get_object_or_404(CardType, id=card_type_id)
        price = Decimal(request.POST.get('price'))

        card_price = CardPrice.objects.filter(card_price=card_type, price=price).first()

        if card_price is not None:
            available_quantity = card_price.quantity
            cart, created = Cart.objects.get_or_create(user=self.request.user)
            cart_item, item_created = CartItem.objects.get_or_create(cart=cart, card=card_price)

            if not item_created:
                if cart_item.amount < available_quantity:
                    cart_item.amount += 1
                    cart_item.save()
                else:
                    messages.error(self.request, "Cannot add more of this item to cart. Maximum quantity reached.")
                    return redirect('cart_view')

            cart_item.price = card_price.price
            cart_item.save()

            return redirect('cart_view')
        else:
            return HttpResponseBadRequest("Invalid card price data.")

    def get(self, request, *args, **kwargs):
        return HttpResponseNotAllowed(['POST'])

class CartView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        try:
            cart = self.request.user.cart
            cart_items = cart.items.all()
            total_quantity = sum(item.amount for item in cart_items)
            total_price = sum(item.card.price * item.amount for item in cart_items)
        except Cart.DoesNotExist:
            cart_items = []
            total_quantity = 0
            total_price = 0

        context = {
            'cart_items': cart_items,
            'total_quantity': total_quantity,
            'total_price': total_price,
        }
        return render(request, 'cart_view.html', context)

class RemoveFromCartView(LoginRequiredMixin, View):
    def post(self, request, cart_item_id):
        cart_item = get_object_or_404(CartItem, id=cart_item_id)
        if cart_item.cart.user == self.request.user:
            cart_item.delete()
            messages.success(request, "Item removed from cart.")
        return redirect('cart_view')


class ClearCartView(LoginRequiredMixin, View):
    def get(self, request):
        cart = self.request.user.cart
        cart.items.all().delete()
        messages.success(request, "Cart cleared successfully.")
        return redirect('cart_view')

@receiver(user_logged_out)
def clear_cart_on_logout(sender, user, request, **kwargs):
    if user.is_authenticated:
        try:
            cart = user.cart
            cart.items.all().delete()
        except Cart.DoesNotExist:
            pass
"""# cart_app/tests.py
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Cart, CartItem
from product_app.models import CardType, CardPrice

class CartItemTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.card_type = CardType.objects.create(card_name='Test Card')
        self.card_price = CardPrice.objects.create(card_price=self.card_type, price=10.0, quantity=5)

    def test_add_to_cart(self):
        self.client.login(username='testuser', password='12345')

        # Simulate adding an item to cart
        response = self.client.post(reverse('add_to_cart', args=[self.card_type.id]), {'price': 10.0})

        # Check if the item is added successfully
        self.assertEqual(response.status_code, 302)  # Expecting a redirect
        self.assertEqual(CartItem.objects.count(), 1)  # Expecting one item in the cart
        self.assertEqual(CartItem.objects.first().card, self.card_price)  # Check if correct card is added

    def test_remove_from_cart(self):
        self.client.login(username='testuser', password='12345')

        # Add an item to cart first
        cart = Cart.objects.create(user=self.user)
        cart_item = CartItem.objects.create(cart=cart, card=self.card_price, amount=1)

        # Simulate removing an item from cart
        response = self.client.post(reverse('remove_from_cart', args=[cart_item.id]))

        # Check if the item is removed successfully
        self.assertEqual(response.status_code, 302)  # Expecting a redirect
        self.assertEqual(CartItem.objects.count(), 0)  # Expecting no items in the cart after removal

    def test_clear_cart(self):
        self.client.login(username='testuser', password='12345')

        # Add some items to cart first
        cart = Cart.objects.create(user=self.user)
        cart_item1 = CartItem.objects.create(cart=cart, card=self.card_price, amount=1)
        cart_item2 = CartItem.objects.create(cart=cart, card=self.card_price, amount=2)

        # Simulate clearing the cart
        response = self.client.get(reverse('clear_cart'))

        # Check if the cart is cleared successfully
        self.assertEqual(response.status_code, 302)  # Expecting a redirect
        self.assertEqual(CartItem.objects.count(), 0)  # Expecting no items in the cart after clearing

    def test_cart_view(self):
        self.client.login(username='testuser', password='12345')

        # Accessing the cart view
        response = self.client.get(reverse('cart_view'))

        # Check if the cart view returns a successful response
        self.assertEqual(response.status_code, 200)  # Expecting a successful response

        # Optionally, check if the context data is correct
        self.assertIn('cart_items', response.context)
        self.assertIn('total_quantity', response.context)
        self.assertIn('total_price', response.context)
"""
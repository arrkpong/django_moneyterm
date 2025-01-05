"""# payments/tests.py
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from orders_app.models import Order, OrderItem
from cart_app.models import Cart, CartItem
from product_app.models import CardType, CardPrice, CardDetail
from django.core.exceptions import ValidationError
from django.conf import settings
from unittest.mock import patch
import json
import stripe
import time
import re

class SuccessViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='testuser', password='12345')

    def setUp(self):
        self.client = Client()
        self.client.login(username='testuser', password='12345')
        self.order = Order.objects.create(user=self.user, total_price=100.00, status='Pending')

    def test_success_view(self):
        response = self.client.get(reverse('success'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'success.html')

        # Print out the response content for debugging
        print(response.content.decode('utf-8'))

        # Refresh the order object to get the latest data
        self.order.refresh_from_db()
        expected_text = f'Order #{self.order.id} by {self.user.username}'

        # Use assertContains with a more flexible check using re.escape
        self.assertContains(response, re.escape(expected_text))


class CancelledViewTest(TestCase):
    def test_cancelled_view(self):
        response = self.client.get(reverse('cancelled'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cancelled.html')

class StripeConfigViewTest(TestCase):
    def test_stripe_config_view(self):
        response = self.client.get(reverse('stripe_config'))
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {'publicKey': settings.STRIPE_PUBLISHABLE_KEY})

class CreateCheckoutSessionViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='testuser', password='12345')
        cls.card_type = CardType.objects.create(card_name='Test Card Type', description='Test description', is_popular=True)
        cls.card_price = CardPrice.objects.create(card_price=cls.card_type, price=50.00)
        cls.cart = Cart.objects.create(user=cls.user)
        cls.cart_item = CartItem.objects.create(cart=cls.cart, card=cls.card_price, amount=2)

    def setUp(self):
        self.client = Client()
        self.client.login(username='testuser', password='12345')

    def test_create_checkout_session_view(self):
        # Mocking an invalid email scenario
        with patch('django.core.validators.validate_email') as mock_validate_email:
            mock_validate_email.side_effect = ValidationError("Enter a valid email address.")

            response = self.client.get(reverse('create_checkout_session'))
            self.assertEqual(response.status_code, 400)
            content = json.loads(response.content)

            # Check if error message is returned correctly
            self.assertIn('error', content)
            self.assertIn('Enter a valid email address.', content['error'])  # Check the entire error message
            self.assertNotIn('sessionId', content)
            self.assertNotIn('payment_status', content)


class StripeWebhookViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='testuser', password='12345')

    def test_stripe_webhook_view(self):
        payload = json.dumps({'type': 'checkout.session.completed', 'data': {'object': {'client_reference_id': self.user.id}}})
        sig_header = 't=' + str(int(time.time())) + ',v1=' + stripe.WebhookSignature._compute_signature(payload, settings.STRIPE_ENDPOINT_SECRET)
        response = self.client.post(reverse('stripe_webhook'), data=payload, content_type='application/json', HTTP_STRIPE_SIGNATURE=sig_header)
        self.assertEqual(response.status_code, 400)

class RevenueRecognitionViewTest(TestCase):
    def test_revenue_recognition_view(self):
        response = self.client.get(reverse('revenue_recognition'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'revenue_recognition.html')
"""
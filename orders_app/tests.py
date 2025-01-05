"""# orders_app/tests.py
from django.test import TestCase
from django.contrib.auth.models import User
from django.utils.timezone import now
from .models import Order, OrderItem, Feedback
from product_app.models import CardType, CardPrice

class OrderModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        cls.user = User.objects.create_user(username='testuser', password='12345')

    def setUp(self):
        # Set up objects for each test method
        self.order = Order.objects.create(
            user=self.user,
            total_price=100.00,
            order_date=now(),
            status='Pending'
        )

    def test_order_str_method(self):
        self.assertEqual(str(self.order), f"Orders #{self.order.pk} by {self.user.username}")

    def test_order_default_status(self):
        self.assertEqual(self.order.status, 'Pending')

    # Add more tests for other fields and behaviors as needed

class OrderItemModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        cls.user = User.objects.create_user(username='testuser', password='12345')  # Add this line
        cls.card_type = CardType.objects.create(card_name='Test Card Type', description='Test description', is_popular=True)
        cls.card_price = CardPrice.objects.create(card_price=cls.card_type, price=50.00)

    def setUp(self):
        # Set up objects for each test method
        self.order = Order.objects.create(
            user=self.user,
            total_price=100.00,
            order_date=now(),
            status='Pending'
        )
        self.order_item = OrderItem.objects.create(
            order=self.order,
            card=self.card_price,
            amount=2,
            price=self.card_price.price * 2
        )

    def test_order_item_str_method(self):
        self.assertEqual(str(self.order_item), f"2 x {self.card_price} in Order #{self.order.pk}")

    # Add more tests for other fields and behaviors as needed

class FeedbackModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        cls.user = User.objects.create_user(username='testuser', password='12345')

    def setUp(self):
        # Set up objects for each test method
        self.order = Order.objects.create(
            user=self.user,
            total_price=100.00,
            order_date=now(),
            status='Pending'
        )
        self.feedback = Feedback.objects.create(
            order=self.order,
            user=self.user,
            rating=5,
            comment='Great service!'
        )

    def test_feedback_str_method(self):
        self.assertEqual(str(self.feedback), f"Feedback for Order #{self.order.pk} by {self.user.username}")

    # Add more tests for other fields and behaviors as needed
"""
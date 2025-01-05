"""# support_app/tests.py
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from support_app.models import Ticket

class SupportAppTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.ticket = Ticket.objects.create(subject='Test Ticket', message='This is a test ticket', customer=self.user)

    def test_create_ticket_view(self):
        url = reverse('create_ticket')

        # Ensure user is logged in before making POST request
        self.client.login(username='testuser', password='testpassword')

        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        # Test POST request to create a ticket
        response = self.client.post(url, {'subject': 'New Test Ticket', 'message': 'This is a new test ticket'})
        self.assertEqual(response.status_code, 302)  # Should redirect after successful creation
        redirected_url = reverse('ticket_responses', kwargs={'ticket_id': Ticket.objects.latest('id').id})
        self.assertRedirects(response, redirected_url)

    def test_ticket_responses_view(self):
        url = reverse('ticket_responses', args=[self.ticket.id])

        # Login before making POST request
        self.client.login(username='testuser', password='testpassword')

        # Test POST request to add response to ticket
        response = self.client.post(url, {'message': 'Response message'})
        self.assertEqual(response.status_code, 302)  # Should redirect after successful response
        redirected_url = reverse('ticket_responses', kwargs={'ticket_id': self.ticket.id})
        self.assertRedirects(response, redirected_url)
"""
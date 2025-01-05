# payments/views.py
from django.shortcuts import render
from django.views import View
from django.views.generic.base import TemplateView
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.http import JsonResponse, HttpResponse, HttpResponseServerError
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.utils.html import strip_tags
from django.conf import settings
from django.contrib.auth.models import User
from orders_app.models import Order, OrderItem
from cart_app.models import CartItem
from payments.models import OrderStatus
import stripe

# Class-based view to display success page after successful payment
class SuccessView(TemplateView):
    template_name = 'success.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            latest_order = Order.objects.filter(user=self.request.user).order_by('-id').first()
            if latest_order:
                context['latest_order'] = latest_order
                context['latest_order_items'] = OrderItem.objects.filter(order=latest_order)
        else:
            print("User is not authenticated on SuccessView")
            print("Session data:", self.request.session.items())
        return context

# Class-based view to display cancelled page after payment is cancelled
class CancelledView(TemplateView):
    template_name = 'cancelled.html'

# Class-based view to return Stripe public key configuration
@method_decorator(csrf_exempt, name='dispatch')
class StripeConfigView(View):
    def get(self, request, *args, **kwargs):
        stripe_config = {'publicKey': settings.STRIPE_PUBLISHABLE_KEY}
        return JsonResponse(stripe_config, safe=False)

# Class-based view to create a checkout session on Stripe
@method_decorator(csrf_exempt, name='dispatch')
class CreateCheckoutSessionView(View):
    def get(self, request, *args, **kwargs):
        domain_url = 'http://localhost:8000/'
        stripe.api_key = settings.STRIPE_SECRET_KEY
        try:
            if not request.user.is_authenticated:
                return JsonResponse({'error': 'User is not authenticated'}, status=401)

            cart_items = CartItem.objects.filter(cart__user=request.user)

            if not cart_items.exists():
                return JsonResponse({'error': 'No items in the cart'}, status=400)

            line_items = []
            for cart_item in cart_items:
                line_item = {
                    'price_data': {
                        'currency': 'thb',
                        'unit_amount': int(cart_item.card.price * 100),
                        'product_data': {
                            'name': str(cart_item.card),
                        },
                    },
                    'quantity': cart_item.amount,
                }
                line_items.append(line_item)

            # Validate user email format
            try:
                validate_email(request.user.email)
            except ValidationError as e:
                return JsonResponse({'error': f"Invalid email address: {e}"}, status=400)

            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card','promptpay'],
                line_items=line_items,
                mode='payment',
                success_url=domain_url + 'success?session_id={CHECKOUT_SESSION_ID}',
                cancel_url=domain_url + 'cancelled/',
                customer_email=request.user.email,
                client_reference_id=request.user.id,
                metadata={
                    'user_id': request.user.id,
                    'username': request.user.username,
                    'customer_name': request.user.get_full_name() if request.user.get_full_name() else str(request.user.username),
                    'customer': str(request.user.email),
                    'description': 'Purchase from your website',
                },
            )

            return JsonResponse({'sessionId': checkout_session['id'], 'payment_status': checkout_session['payment_status']})
        
        except stripe.error.StripeError as e:
            return JsonResponse({'error': str(e)}, status=500)
        
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

#shipping_address_collection={'allowed_countries': ['US', 'CA', 'TH'],},
# Class-based view to handle Stripe webhook events
@method_decorator(csrf_exempt, name='dispatch')
class StripeWebhookView(View):
    def post(self, request, *args, **kwargs):
        print("Stripe webhook received")
        stripe.api_key = settings.STRIPE_SECRET_KEY
        endpoint_secret = settings.STRIPE_ENDPOINT_SECRET
        payload = request.body
        sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')

        if not sig_header:
            return HttpResponse(status=400)

        event = None

        try:
            event = stripe.Webhook.construct_event(
                payload, sig_header, endpoint_secret
            )
        except ValueError as e:
            print("Invalid payload:", e)
            return HttpResponse(status=400)
        except stripe.error.SignatureVerificationError as e:
            print("Invalid signature:", e)
            return HttpResponse(status=400)

        event_type = event['type']
        print(f"Handling event type: {event_type}")

        try:
            if event_type == 'charge.succeeded':
                print("Charge was successful:", event['id'])
            elif event_type == 'checkout.session.completed':
                checkout_session = event['data']['object']
                user_id = checkout_session.get('client_reference_id')
                if not user_id:
                    return JsonResponse({'error': 'Client reference ID is missing'}, status=400)

                user = User.objects.get(pk=user_id)
                if not user.is_authenticated:
                    print("User is not authenticated during webhook processing")
                    return JsonResponse({'error': 'User is not authenticated'}, status=401)

                print(f"User {user.username} is authenticated and checkout session completed.")

                order = Order.objects.create(user_id=user_id, total_price=0, status='completed')
                cart_items = CartItem.objects.filter(cart__user_id=user_id)
                for cart_item in cart_items:
                    active_card_details = cart_item.card.card_details.filter(is_active=True)[:cart_item.amount]
                    for active_card_detail in active_card_details:
                        order_item = OrderItem.objects.create(
                            order=order,
                            card=cart_item.card,
                            amount=1,
                            price=cart_item.card.price,
                            serial_number=active_card_detail.serial_number,
                            pin=active_card_detail.pin
                        )
                        active_card_detail.is_active = False
                        active_card_detail.save()
                        order.total_price += order_item.price
                        order.save()
                        
                cart_items = CartItem.objects.filter(cart__user_id=user_id)
                cart_items.delete()

                # Create OrderStatus for 'completed' status
                OrderStatus.objects.create(order=order, status=OrderStatus.COMPLETED)

                subject = 'Your order has been placed successfully'
                message = render_to_string('email/order_placed_email.html', {'order': order})
                from_email = settings.DEFAULT_FROM_EMAIL
                to_email = [user.email]
                send_mail(subject, strip_tags(message), from_email, to_email, html_message=message)
            elif event_type == 'payment_intent.succeeded':
                print("Payment intent was successful:", event['id'])
            elif event_type == 'payment_intent.created':
                print("Payment intent was created:", event['id'])
            elif event_type == 'checkout.session.payment_failed':
                print("Payment failed:", event['id'])
            elif event_type == 'checkout.session.cancelled':
                print("Payment was cancelled by the customer:", event['id'])
            else:
                print(f"Unhandled event type: {event_type}")
        except Exception as e:
            return HttpResponseServerError(str(e))

        return HttpResponse(status=200)

# Class-based view to display revenue recognition
class RevenueRecognitionView(View):
    def get(self, request, *args, **kwargs):
        stripe.api_key = settings.STRIPE_SECRET_KEY
        try:
            charges = stripe.Charge.list(limit=10, expand=['data.customer'])
            return render(request, 'revenue_recognition.html', {'charges': charges.data})
        except Exception as e:
            return render(request, 'revenue_recognition.html', {'error': str(e)})

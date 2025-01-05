# payments/urls.py

from django.urls import path
from payments.views import StripeConfigView,CreateCheckoutSessionView,SuccessView,CancelledView,StripeWebhookView,RevenueRecognitionView

urlpatterns = [
    path('config/', StripeConfigView.as_view(), name='stripe_config'),
    path('create-checkout-session/', CreateCheckoutSessionView.as_view(), name='create_checkout_session'),
    path('success/', SuccessView.as_view(), name='success'),
    path('cancelled/', CancelledView.as_view(), name='cancelled'),
    path('payments/webhook/', StripeWebhookView.as_view(), name='stripe_webhook'),
    path('webhook/', StripeWebhookView.as_view(), name='webhook'),
    path('revenue-recognition/', RevenueRecognitionView.as_view(), name='revenue_recognition'),
]

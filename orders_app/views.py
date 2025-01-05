from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse
from django.contrib import messages
from django.db.models import Sum
from django.utils.timezone import make_aware, now
from datetime import datetime, timedelta
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings
from .models import Order, OrderItem, Feedback
import stripe

class OrderHistoryView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        orders = Order.objects.filter(user=request.user).order_by('-order_date')
        order_items = OrderItem.objects.filter(order__in=orders)
        return render(request, 'order_history.html', {'orders': orders, 'order_items': order_items})


class ShowCardDetailsView(LoginRequiredMixin, View):
    def get(self, request, card_id, *args, **kwargs):
        try:
            order_item = OrderItem.objects.get(order__user=request.user, card_id=card_id)
            card_detail = order_item.card.card_detail
            card_details = f"Serial Number: {card_detail.serial_number}, PIN: {card_detail.pin}"
            return HttpResponse(card_details)
        except OrderItem.DoesNotExist:
            return HttpResponse("No information found or there is more than 1 item.")


class FeedbackFormView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        order_id = request.GET.get('order_id')
        if order_id:
            try:
                Order.objects.get(pk=order_id)
                return render(request, 'feedback_form.html', {'order_id': order_id})
            except Order.DoesNotExist:
                return HttpResponse("Order matching query does not exist.")
        else:
            return HttpResponse("No order ID provided in the query string. Please select an order to provide feedback.")

    def post(self, request, *args, **kwargs):
        order_id = request.POST.get('order_id')
        if order_id:
            try:
                order = Order.objects.get(pk=order_id)
                existing_feedback = Feedback.objects.filter(order=order, user=request.user)
                if existing_feedback.exists():
                    messages.warning(request, "You have already submitted feedback for this order.")
                    return redirect(reverse('order_history'))

                rating = request.POST.get('rating')
                comment = request.POST.get('comment')

                if not rating:
                    messages.error(request, "Rating is required.")
                    return render(request, 'feedback_form.html', {'order_id': order_id, 'comment': comment})

                try:
                    rating = int(rating)
                    if rating < 1 or rating > 5:
                        messages.error(request, "Rating must be between 1 and 5.")
                        return render(request, 'feedback_form.html', {'order_id': order_id, 'comment': comment})
                except ValueError:
                    messages.error(request, "Rating must be an integer between 1 and 5.")
                    return render(request, 'feedback_form.html', {'order_id': order_id, 'comment': comment})

                feedback = Feedback.objects.create(order=order, user=request.user, rating=rating, comment=comment)
                return redirect(reverse('thank_you'))
            except Order.DoesNotExist:
                return HttpResponse("Order matching query does not exist.")
        else:
            return HttpResponse("No order ID provided. Please select an order to provide feedback.")


class ThankYouView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'thank_you.html')


class SalesSummaryView(View):
    def get(self, request, *args, **kwargs):
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')

        if start_date and end_date:
            try:
                start_date = make_aware(datetime.strptime(start_date, '%Y-%m-%d'))
                end_date = make_aware(datetime.strptime(end_date, '%Y-%m-%d')) + timedelta(days=1)
            except ValueError:
                start_date = now().replace(hour=0, minute=0, second=0, microsecond=0)
                end_date = now()
        else:
            start_date = now().replace(hour=0, minute=0, second=0, microsecond=0)
            end_date = now()

        total_sales = Order.objects.filter(order_date__range=(start_date, end_date)).aggregate(Sum('total_price'))['total_price__sum'] or 0

        try:
            stripe.api_key = settings.STRIPE_SECRET_KEY
            stripe_charges = stripe.Charge.list(
                created={
                    'gte': int(start_date.timestamp()),
                    'lt': int(end_date.timestamp()),
                },
                limit=100
            )

            vat_total = sum(self.calculate_vat_amount(charge) for charge in stripe_charges.auto_paging_iter())
        except stripe.error.StripeError as e:
            vat_total = 0

        context = {
            'total_sales': total_sales,
            'start_date': start_date.strftime('%Y-%m-%d'),
            'end_date': end_date.strftime('%Y-%m-%d'),
            'vat_total': vat_total,
        }

        return render(request, 'sales_summary.html', context)

    @staticmethod
    def calculate_vat_amount(charge):
        if charge.currency.lower() == 'usd':
            vat_amount = charge.amount * 0.0025
        else:
            vat_amount = 0
        return vat_amount

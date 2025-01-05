# products_app/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Count, Value, Q
from django.db.models.functions import Coalesce
from product_app.models import CardType, Advertisement
from django.core.exceptions import ValidationError
from django.http import HttpResponse
from django.urls import reverse

class IndexView(View):
    def get(self, request):
        popular_card_types = CardType.objects.filter(is_popular=True)
        advertisements = Advertisement.objects.order_by('-created_at')[:5]
        return render(request, "index.html", {'popular_card_types': popular_card_types, 'carousel_ads': advertisements})


class ProductsView(View):
    def get(self, request):
        all_card_types = CardType.objects.all().order_by('card_name')
        paginator = Paginator(all_card_types, 4)
        page_number = request.GET.get('page', 1)
        
        try:
            card_types = paginator.page(page_number)
        except PageNotAnInteger:
            card_types = paginator.page(1)
        except EmptyPage:
            card_types = paginator.page(paginator.num_pages)
        
        return render(request, 'products.html', {'card_types': card_types})


class ProductDetailView(View):
    def get(self, request, card_name_id):
        card_type = get_object_or_404(CardType, pk=card_name_id)
        counts_card_type = card_type.card_prices.annotate(count=Coalesce(Count('card_details', filter=Q(card_details__is_active=True)), Value(0))).values('price', 'count')
        
        return render(request, 'product_detail.html', {'card_type': card_type, 'counts_card_type': counts_card_type})


class AboutView(View):
    def get(self, request):
        return render(request, 'about.html')


class SearchResultsView(View):
    def get(self, request):
        query = request.GET.get('q')
        try:
            if query:
                results = CardType.objects.filter(card_name__icontains=query)
            else:
                results = CardType.objects.none()
        except ValidationError:
            results = CardType.objects.none()
        
        return render(request, 'search_results.html', {'results': results, 'query': query})


class CookiePolicyView(View):
    def get(self, request):
        return render(request, 'cookie_policy.html')


class PrivacyPolicyView(View):
    def get(self, request):
        return render(request, 'privacy_policy.html')

'''class CookieView(View):
    def get(self, request, *args, **kwargs):
        cookie_value = request.COOKIES.get('cookie_name', 'default_value')
        return HttpResponse(f"Cookie value: {cookie_value}")

    def post(self, request, *args, **kwargs):
        accept_cookies = request.POST.get('acceptCookies')
        if accept_cookies == 'true':
            cookie_value = 'accepted'
        elif accept_cookies == 'false':
            cookie_value = 'rejected'
        else:
            return HttpResponse("Invalid request", status=400)

        response = HttpResponse(f"Cookie value: {cookie_value}")
        response.set_cookie('cookie_name', cookie_value, max_age=3600, secure=True, samesite='Lax')
        return response'''

    
def custom_404(request, exception):
    return render(request, '404.html', status=404)

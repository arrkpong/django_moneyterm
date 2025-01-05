#Products_App/urls.py
from django.urls import path
from product_app import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('products/', views.ProductsView.as_view(), name='products'),
    path('products/detail/<int:card_name_id>/', views.ProductDetailView.as_view(), name='product_detail'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('search/', views.SearchResultsView.as_view(), name='search'),
    path('cookie_policy/', views.CookiePolicyView.as_view(), name='cookie_policy'),
    path('privacy_policy/', views.PrivacyPolicyView.as_view(), name='privacy_policy'),
    #path('cookie/', views.CookieView.as_view(), name='cookie'),
]

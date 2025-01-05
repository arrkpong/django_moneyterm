from django.urls import path
from orders_app import views

urlpatterns = [
    path('order_history/', views.OrderHistoryView.as_view(), name='order_history'),
    path('show_card_details/<int:card_id>/', views.ShowCardDetailsView.as_view(), name='show_card_details'),
    path('feedback/', views.FeedbackFormView.as_view(), name='feedback_form'),
    path('thank_you/', views.ThankYouView.as_view(), name='thank_you'),
    path('submit_feedback/', views.FeedbackFormView.as_view(), name='submit_feedback'),
    path('sales_summary/', views.SalesSummaryView.as_view(), name='sales_summary'),
]

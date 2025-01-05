# urls.py
from django.urls import path
from support_app.views import SupportView, CreateTicketView, TicketResponsesView, TicketListView, CloseTicketView

urlpatterns = [
    path('support/', SupportView.as_view(), name='support'),
    path('support/create_ticket/', CreateTicketView.as_view(), name='create_ticket'),
    path('support/tickets/<int:ticket_id>/', TicketResponsesView.as_view(), name='ticket_responses'),
    path('support/tickets/', TicketListView.as_view(), name='ticket_list'),
    path('support/tickets/<int:ticket_id>/close/', CloseTicketView.as_view(), name='close_ticket'),
    # Other paths as needed
]

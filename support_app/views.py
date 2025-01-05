# support_app/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib import messages
from django.core.validators import FileExtensionValidator
from django.core.exceptions import ValidationError
from django.contrib.auth.decorators import login_required 
from django.utils.decorators import method_decorator
from support_app.models import Ticket, Response

class LoginRequiredMixin:
    @classmethod
    def as_view(cls, **kwargs):
        view = super().as_view(**kwargs)
        return login_required(view)

class SupportView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'support.html')

class CreateTicketView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'create_ticket.html')

    def post(self, request):
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        image = request.FILES.get('image')

        # Validate file extension if image is uploaded
        if image:
            validator = FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'gif'])
            try:
                validator(image)
            except ValidationError:
                messages.error(request, 'Invalid file format. Please upload a valid image file.')
                return redirect('create_ticket')  # Redirect instead of render to prevent form resubmission

        ticket = Ticket(subject=subject, message=message, customer=request.user)

        # Save image if it exists
        if image:
            ticket.image = image

        ticket.save()
        messages.success(request, 'Ticket created successfully!')
        return redirect('ticket_responses', ticket_id=ticket.id)

class TicketResponsesView(LoginRequiredMixin, View):
    def get(self, request, ticket_id):
        ticket = get_object_or_404(Ticket, id=ticket_id)
        responses = ticket.responses.all()

        # Check ticket status and display appropriate message
        if ticket.status == 'Closed':
            messages.warning(request, "This ticket has been closed and no further responses are allowed.")

        return render(request, 'ticket_responses.html', {'ticket': ticket, 'responses': responses})

    def post(self, request, ticket_id):
        ticket = get_object_or_404(Ticket, id=ticket_id)
        message = request.POST.get('message')
        image = request.FILES.get('image')

        # Validate file extension if image is uploaded
        if image:
            validator = FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'gif'])
            try:
                validator(image)
            except ValidationError:
                messages.error(request, 'Invalid file format. Please upload a valid image file.')
                return redirect('ticket_responses', ticket_id=ticket.id)

        response = Response(ticket=ticket, message=message, image=image, responder=request.user)
        response.save()
        messages.success(request, 'Response added successfully!')
        return redirect('ticket_responses', ticket_id=ticket.id)

class TicketListView(LoginRequiredMixin, View):
    def get(self, request):
        if request.user.is_superuser or request.user.is_staff:
            tickets = Ticket.objects.filter(status='Open')
        else:
            tickets = Ticket.objects.filter(customer=request.user)

        return render(request, 'ticket_list.html', {'tickets': tickets})

class CloseTicketView(LoginRequiredMixin, View):
    def post(self, request, ticket_id):
        if request.user.is_superuser or request.user.is_staff:
            ticket = get_object_or_404(Ticket, id=ticket_id)
            ticket.status = 'Closed'
            ticket.save()
            messages.success(request, f'Ticket {ticket_id} has been closed successfully.')
        else:
            messages.error(request, 'You do not have permission to close this ticket.')

        return redirect('ticket_list')

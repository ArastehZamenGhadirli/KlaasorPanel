from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from .models import Ticket

@shared_task
def send_ticket_notification_email(email, ticket_id):
    
    try:
        ticket = Ticket.objects.get(id=ticket_id)
        subject = f"New Ticket: {ticket.subject}"
        message = (
            f"New support ticket submitted by {ticket.user.email}.\n"
            f"Category: {ticket.get_category_display()}\n"
            f"Status: {ticket.status}\n"
            "Login to admin panel to view."
        )
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [email])
    except Ticket.DoesNotExist:
        pass
    



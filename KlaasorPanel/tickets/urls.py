from django.urls import path
from .views import CreateTicketMessageView

urlpatterns = [
    path('tickets/<int:ticket_id>/messages/', CreateTicketMessageView.as_view(), name='create-ticket-message'),
]
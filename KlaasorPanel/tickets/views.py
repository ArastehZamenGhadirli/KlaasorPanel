from django.shortcuts import render
from django.shortcuts import render
from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.generics import (
    ListAPIView,
    RetrieveAPIView,
    CreateAPIView,
    DestroyAPIView,
    UpdateAPIView,
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.views import APIView

from accounts.serializers import AccountsSerializer
from rest_framework.permissions import (
    IsAuthenticated,
    IsAdminUser,
    IsAuthenticatedOrReadOnly,
    AllowAny,
)
from django_filters.rest_framework import DjangoFilterBackend  # type: ignore
from rest_framework import filters
from accounts.models import CustomUser
from  tickets.models import Ticket , TicketMessage
from tickets.serializers import TicketSerializer,TicketMessageSerializer
from rest_framework_simplejwt.tokens import RefreshToken  # for JWT Athutorization
from rest_framework.response import Response
from django.core.cache import cache
from .models import Ticket
from accounts.models import Team
from .task import send_ticket_notification_email
from rest_framework import status
#creating ticket view 


class CreateTicketView(CreateAPIView):
    """
    Authenticated users can create a new support ticket.
    If a bootcamp is provided, the ticket is linked to it.
    Once a ticket is created, all relevant support team members
    (based on category) will be notified via email using Celery,
    with Redis caching to avoid duplicate emails within a short window.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = TicketSerializer(data=request.data)
        if serializer.is_valid():
            ticket = serializer.save(user=request.user)

            # Notify team members
            team_members = Team.objects.filter(role=ticket.category)
            for member in team_members:
                cache_key = f"notified_ticket_{ticket.id}_{member.id}"
                if not cache.get(cache_key):
                    send_ticket_notification_email.delay(member.email, ticket.id)
                    cache.set(cache_key, True, timeout=600)  # 10 minutes

            return Response({"message": "Ticket created and team notified."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    



class CreateTicketMessageView(APIView):
    """
    Authenticated users can reply to a ticket.
    Each message can contain text, a file attachment, or both.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, ticket_id):
        try:
            ticket = Ticket.objects.get(id=ticket_id)
        except Ticket.DoesNotExist:
            return Response({"error": "Ticket not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = TicketMessageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(ticket=ticket, sender=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



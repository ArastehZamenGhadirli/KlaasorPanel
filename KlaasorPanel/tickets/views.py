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
from tickets.serializers import TicketSerializer,TicketMessageSerilzer
from rest_framework_simplejwt.tokens import RefreshToken  # for JWT Athutorization
from rest_framework.response import Response


#creating ticket view 


class CreateTicketView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    

#answering ticket view \

class AnswerTicketView(CreateAPIView):
    pass 



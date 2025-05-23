from django.shortcuts import render
from django.shortcuts import render
from orders.models import Bootcamp, BootcampMembership
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
from django_filters.rest_framework import DjangoFilterBackend  # type: ignore
from rest_framework import filters
from rest_framework_simplejwt.tokens import RefreshToken  # for JWT Athutorization
from rest_framework.response import Response
from accounts.permissions import (
    IsMentor,
    IsNormal,
    IsRegisterSupport,
    IsTeacherOrMentor,
    IsTicketSupport,
)
from django.core.cache import cache
import random
from .models import (
    Invoice ,
    Payment,
    OfflinePaymentDetail
)
from .serializers import InvoiceSerializer , PaymentSerializer , OfflinePaymentDetailSerializer
from rest_framework.permissions import (
    IsAuthenticated,
    IsAdminUser,
    IsAuthenticatedOrReadOnly,
    AllowAny,
)

from rest_framework.generics import (
    ListAPIView, CreateAPIView, RetrieveAPIView, RetrieveUpdateAPIView
)
from rest_framework.permissions import IsAuthenticated
from accounts.permissions import IsRegisterSupport
from .models import Invoice, Payment, OfflinePaymentDetail
from .serializers import (
    InvoiceSerializer, PaymentSerializer, OfflinePaymentDetailSerializer
)


class InvoiceListView(ListAPIView):
    """
    List all invoices for the authenticated user.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = InvoiceSerializer

    def get_queryset(self):
        return Invoice.objects.filter(user=self.request.user)


class InvoiceCreateView(CreateAPIView):
    """
    Allows register support to create a new invoice for a user.
    """
    permission_classes = [IsAuthenticated,IsRegisterSupport]
    serializer_class = InvoiceSerializer
    queryset = Invoice.objects.all()


class PaymentCreateView(CreateAPIView):
    """
    Allows a user to submit a payment for an invoice.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()


class OfflinePaymentDetailCreateView(CreateAPIView):
    """
    Allows a user to submit offline payment details including tracking code and receipt image.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = OfflinePaymentDetailSerializer
    queryset = OfflinePaymentDetail.objects.all()


class PaymentHistoryView(ListAPIView):
    """
    Lists all payments of the authenticated user.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = PaymentSerializer

    def get_queryset(self):
        return Payment.objects.filter(user=self.request.user)


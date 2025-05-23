from django.urls import path
from .views import (
    InvoiceListView,
    InvoiceCreateView,
    PaymentCreateView,
    OfflinePaymentDetailCreateView,
    PaymentHistoryView,
)

urlpatterns = [
    path('invoices/', InvoiceListView.as_view(), name='invoice-list'),
    path('invoices/create/', InvoiceCreateView.as_view(), name='invoice-create'),
    path('payments/create/', PaymentCreateView.as_view(), name='payment-create'),
    path('payments/offline/', OfflinePaymentDetailCreateView.as_view(), name='offline-payment-create'),
    path('payments/history/', PaymentHistoryView.as_view(), name='payment-history'),
]
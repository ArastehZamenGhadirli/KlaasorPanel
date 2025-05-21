from django.urls import path
from .views import (
    UserTransactionSummaryView,
    InvoiceCreateView,
    InvoiceListView,
    InvoiceDetailView,
    OnlinePaymentView,
    OfflinePaymentSubmissionView,
    OfflinePaymentListView,
)

urlpatterns = [
    path("summary/", UserTransactionSummaryView.as_view(), name="transaction-summary"),
    path("invoices/create/", InvoiceCreateView.as_view(), name="create-invoice"),
    path("invoices/", InvoiceListView.as_view(), name="list-invoices"),
    path("invoices/<int:pk>/", InvoiceDetailView.as_view(), name="invoice-detail"),
    path("payments/online/", OnlinePaymentView.as_view(), name="online-payment"),
    path(
        "payments/offline/",
        OfflinePaymentSubmissionView.as_view(),
        name="offline-payment",
    ),
    path(
        "payments/offline/list/",
        OfflinePaymentListView.as_view(),
        name="offline-payment-list",
    ),
]

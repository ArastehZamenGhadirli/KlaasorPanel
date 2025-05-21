from django.db import models
from accounts.models import CustomUser 
# Create your models here.

class Invoice(models.Model):
    """
    Represents a financial invoice issued to a user, typically created by support staff.

    Attributes:
        user (ForeignKey): The user for whom the invoice is issued.
        title (str): A short title or reason for the invoice (e.g., "Bootcamp Payment").
        amount (int): Total amount in Rials.
        description (str): Optional additional information.
        is_paid (bool): Whether the invoice has been paid.
        created_at (datetime): Timestamp when the invoice was created.
    """
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="invoices")
    title = models.CharField(max_length=255)
    amount = models.PositiveIntegerField()
    description = models.TextField(blank=True)
    is_paid = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Invoice #{self.id} - {self.user.email}"


class Payment(models.Model):
    """
    Represents a user's payment against a specific invoice.

    Attributes:
        user (ForeignKey): The user who made the payment.
        invoice (ForeignKey): The invoice associated with this payment.
        amount (int): The amount paid.
        method (str): The method used for payment (online/offline).
        is_verified (bool): Whether the payment is verified (used for offline payments).
        created_at (datetime): Timestamp when the payment was submitted.
    """
    class PaymentMethod(models.TextChoices):
        ONLINE = 'ONLINE', 'Online'
        OFFLINE = 'OFFLINE', 'Offline'

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="payments") 
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name="payments") #every invoice can have many payment (age ghesti bashe hameshon miyad dar yek invoice )
    amount = models.PositiveIntegerField()
    method = models.CharField(max_length=10, choices=PaymentMethod.choices)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email} - {self.amount} - {self.method}"


class OfflinePaymentDetail(models.Model):
    """
    Stores additional information for offline payments such as receipt and tracking code.

    Attributes:
        payment (OneToOne): The payment this detail belongs to.
        tracking_code (str): A reference or tracking number for the transaction.
        receipt_image (Image): An uploaded image of the payment receipt.
    """
    payment = models.OneToOneField(Payment, on_delete=models.CASCADE, related_name="offline_detail")
    tracking_code = models.CharField(max_length=50)
    receipt_image = models.ImageField(upload_to="payment_receipts/")

    def __str__(self):
        return f"Offline Detail for Payment #{self.payment.id}"

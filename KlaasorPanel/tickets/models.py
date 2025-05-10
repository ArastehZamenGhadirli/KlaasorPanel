from django.db import models
from accounts.models import CustomUser, Team
from django.conf import settings
from orders.models import Bootcamp

# Create your models here.


class Ticket(models.Model):

    TICKET_STATUS_CHOICES = (
        ("OPEN", "Open"),
        ("CLOSED", "Closed"),
        ("PENDING", "Pending"),
        ("ANSWERED", "Answered"),
    )

    SUPPORT_CATEGORIES = [
        (Team.TeamRole.FINANCIAL, "Financial Support"),
        (Team.TeamRole.TICKET, "Ticket Support"),
        (Team.TeamRole.REGISTER, "Registration Support"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="CustomUser_Ticket", on_delete=models.CASCADE
    )
    subject = models.CharField(max_length=255)
    category = models.CharField(
        max_length=20,
        choices=SUPPORT_CATEGORIES,
        null=True,
        blank=True,
        help_text="نوع پشتیبانی مرتبط با تیکت",
    )
    bootcamp = models.ForeignKey(
        Bootcamp,
        on_delete=models.SET_NULL,  # A ticket may or may not be related to a bootcamp.If the related Bootcamp is deleted, you don't want the ticket itself to be deleted (that would be risky).
        null= True,
        blank=True,
        related_name="Bootcamp_Ticket",
        help_text="اگر مقدار نداشته باشه، تیکت عمومی است.",
    )

    status = models.CharField(
        max_length=10, choices=TICKET_STATUS_CHOICES, default='OPEN'
    )
    created_at = models.DateTimeField(auto_now_add=True)    
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f"Ticket #{self.id} - {self.subject}"


class TicketMessage(models.Model):

        ticket = models.ForeignKey(Ticket, related_name='Ticket_TicketMessage', on_delete=models.CASCADE)
        sender = models.ForeignKey( settings.AUTH_USER_MODEL , related_name= 'CustomUser_Sender' , on_delete= models.CASCADE)
        text = models.TextField(blank=True)
        attachment = models.FileField()
        created_at = models.DateTimeField(auto_now_add=True)




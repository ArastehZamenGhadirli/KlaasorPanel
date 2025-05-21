from rest_framework.serializers  import ModelSerializer
from accounts.models import Team  , CustomUser
from tickets.models import  Ticket , TicketMessage 
from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError
from rest_framework import permissions
from .models import Ticket , TicketMessage


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ['subject', 'category', 'bootcamp']  
    

class TicketMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketMessage
        fields = ['ticket', 'text', 'attachment']
        extra_kwargs = {
            'text': {'required': False},
            'attachment': {'required': False},
        }

    def validate(self, data):
        if not data.get('text') and not data.get('attachment'):
            raise serializers.ValidationError("Either 'text' or 'attachment' must be provided.")
        return data



        
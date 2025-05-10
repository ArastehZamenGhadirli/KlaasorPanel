from rest_framework.serializers  import ModelSerializer
from accounts.models import Team  , CustomUser
from tickets.models import  Ticket , TicketMessage 
from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError
from rest_framework import permissions



class TicketSerializer(ModelSerializer):
    class Meta :
        Model = Ticket , 
        feilds = '__all__',
    

class TicketMessageSerilzer(ModelSerializer):
    pass



        
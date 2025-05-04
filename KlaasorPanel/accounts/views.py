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

from accounts.serializers import AccountsSerializer
from rest_framework.permissions import (
    IsAuthenticated,
    IsAdminUser,
    IsAuthenticatedOrReadOnly,
    AllowAny,
)
from django_filters.rest_framework import DjangoFilterBackend # type: ignore
from rest_framework import filters
from accounts.models import CustomUser , Team
from accounts.serializers import AccountsSerializer


class CreateCustomUserView(CreateAPIView):
    """
    Register (signup) View For CustomUser
    """
    permission_classes = [AllowAny]
    queryset = CustomUser.all()
    #serializer_class = AccountsSerializer


#Editing personal information view
class UpdateCustomUSerView(UpdateAPIView):
    pass
#sign_in --->otp
#sign_out 
#sign_in --->password
class 
#changepassword OR forget password (newpassword , repeated password)  








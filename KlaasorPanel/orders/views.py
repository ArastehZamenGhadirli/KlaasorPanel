from django.shortcuts import render
from orders.models import Bootcamp , BootcampMembership
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
from .models import Bootcamp , BootcampMembership , BootcampRegistrationRequest
from rest_framework import serializers
from .serializers import BootcampCreateSerilazer ,BootcampRegisterSerilazer ,BootcampRegistrationRequestSerializer
from accounts.permissions import *
from rest_framework.permissions import (
    IsAuthenticated,
    IsAdminUser,
    IsAuthenticatedOrReadOnly,
    AllowAny,
)
# Create your views here.


class BootcampRegisterPublicView(CreateAPIView):
    queryset = BootcampRegistrationRequest.objects.all()
    serializer_class = BootcampRegistrationRequestSerializer
    permission_classes = []  # No auth required



class AdminCreateBootcamp(CreateAPIView):
    queryset = Bootcamp.objects.all()
    serializer_class = BootcampCreateSerilazer
    permission_classes = [
        IsAuthenticated,
        HasGroupPermission(['REGISTER', 'SUPERUSER'])
    ]
    



class AdminDeleteBootcamp(DestroyAPIView):
    pass

class AdminUpdateBootcamp(UpdateAPIView):
    pass



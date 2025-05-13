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
# Create your views here.



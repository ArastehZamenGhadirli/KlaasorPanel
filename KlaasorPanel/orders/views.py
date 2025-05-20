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
    Bootcamp,
    BootcampMembership,
    BootcampRegistrationRequest,
    BootcampCategory,
)
from rest_framework import serializers
from .serializers import (
    BootcampSerilazer,
    BootcampRegisterSerilazer,
    BootcampRegistrationRequestSerializer,
    BootcampCategorySerialzer,
    BootcampDetailSerializer
)
from accounts.permissions import *
from rest_framework.permissions import (
    IsAuthenticated,
    IsAdminUser,
    IsAuthenticatedOrReadOnly,
    AllowAny,
)
from django.core.mail import send_mail
from django.db import transaction
from accounts.models import CustomUser 
from orders.tasks import  send_registration_email , send_sms_to_user

# Create your views here.


# every one can send request for being register in a bootcamp
class BootcampRegisterPublicView(CreateAPIView):
    queryset = BootcampRegistrationRequest.objects.all()
    serializer_class = BootcampRegistrationRequestSerializer
    permission_classes = []  # No auth required


# admin create a bootcamp
class AdminCreateBootcampView(CreateAPIView):
    queryset = Bootcamp.objects.all()
    serializer_class = BootcampSerilazer
    permission_classes = [
        IsAuthenticated,
        HasGroupPermission(["REGISTER", "SUPERUSER"]),
    ]


# admin delete a bootcamp
class AdminDeleteBootcampView(DestroyAPIView):
    queryset = Bootcamp.objects.all()
    serializer_class = BootcampSerilazer
    permission_classes = [
        IsAuthenticated,
        HasGroupPermission(["REGISTER", "SUPERUSER"]),
    ]


# admin Update a Bootcmap
class AdminUpdateBootcampView(UpdateAPIView):
    queryset = Bootcamp.objects.all()
    serializer_class = BootcampSerilazer
    permission_classes = [
        IsAuthenticated,
        HasGroupPermission(["REGISTER", "SUPERUSER"]),
    ]


# admin create the catagory of bootcamps
class AdminCreateCatagoryView(CreateAPIView):
    queryset = BootcampCategory.objects.all()
    serializer_class = BootcampCategorySerialzer
    permission_classes = [
        IsAuthenticated,
        HasGroupPermission(["REGISTER", "SUPERUSER"]),
    ]


# admin edit  the catagory of bootcamps
class AdminEditCatagoryView(UpdateAPIView):
    queryset = BootcampCategory.objects.all()
    serializer_class = BootcampCategorySerialzer
    permission_classes = [
        IsAuthenticated,
        HasGroupPermission(["REGISTER", "SUPERUSER"]),
    ]


# admin delete  the catagory of bootcamps
class AdminDeleteCatagoryView(DestroyAPIView):
    queryset = BootcampCategory.objects.all()
    serializer_class = BootcampCategorySerialzer
    permission_classes = [
        IsAuthenticated,
        HasGroupPermission(["REGISTER", "SUPERUSER"]),
    ]


class ListCaragoryBootcampView(ListAPIView):
    queryset = BootcampCategory.objects.all()
    serializer_class = BootcampCategorySerialzer
    permission_classes = [AllowAny]


class DetailBootcmapView(RetrieveAPIView):
    queryset = Bootcamp.objects.all()
    serializer_class = BootcampDetailSerializer
    permission_classes = [AllowAny]


class ListRegisteredBootcampView(ListAPIView):
    """
    Lists bootcamps that the authenticated user is registered in as a STUDENT.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = BootcampSerilazer

    def get_queryset(self):
        return BootcampMembership.objects.filter(
            user=self.request.user,
            role=BootcampMembership.Role.STUDENT
        ).select_related('bootcamp').values_list('bootcamp', flat=True)




class ApproveBootcampRegistrationView(APIView):
    """
    Register Support approves a bootcamp registration request.
    - Creates user (if needed)
    - Adds to bootcamp
    - Decreases capacity
    - Sends SMS and Email
    """
    permission_classes = [IsRegisterSupport]

    def post(self, request, registration_id):
        try:
            registration = BootcampRegistrationRequest.objects.get(id=registration_id)
        except BootcampRegistrationRequest.DoesNotExist:
            return Response({'error': 'درخواست یافت نشد.'}, status=404)

        if registration.status == BootcampRegistrationRequest.Status.APPROVED:
            return Response({'error': 'این درخواست قبلاً تایید شده است.'}, status=400)

        bootcamp = registration.bootcamp

        if bootcamp.capacity <= 0:
            return Response({'error': 'ظرفیت بوت‌کمپ تکمیل شده است.'}, status=400)

        with transaction.atomic():
            # 1. Create or fetch user
            user, created = CustomUser.objects.get_or_create(
                email=registration.email,
                defaults={'phone_number': registration.phone_number, 'username': registration.email}
            )

            # 2. Create membership
            BootcampMembership.objects.create(
                user=user,
                bootcamp=bootcamp,
                role=BootcampMembership.Role.STUDENT
            )

            # 3. Reduce bootcamp capacity
            bootcamp.capacity -= 1
            bootcamp.save()

            # 4. Update registration status
            registration.status = BootcampRegistrationRequest.Status.APPROVED
            registration.save()

        # 5. Trigger notifications
        send_sms_to_user.delay(registration.phone_number)
        send_registration_email.delay(registration.email)

        return Response({'message': 'درخواست با موفقیت تایید شد.'}, status=200)
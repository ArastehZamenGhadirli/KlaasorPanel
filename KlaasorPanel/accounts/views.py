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
from rest_framework.views import APIView

from accounts.serializers import AccountsSerializer
from rest_framework.permissions import (
    IsAuthenticated,
    IsAdminUser,
    IsAuthenticatedOrReadOnly,
    AllowAny,
)
from django_filters.rest_framework import DjangoFilterBackend  # type: ignore
from rest_framework import filters
from accounts.models import CustomUser, Team
from accounts.serializers import AccountsSerializer, SignInSerializer, SignUpSerializer
from rest_framework_simplejwt.tokens import RefreshToken  # for JWT Athutorization
from rest_framework.response import Response
from .permissions import (
    IsMentor,
    IsNormal,
    IsRegisterSupport,
    IsTeacherOrMentor,
    IsTicketSupport,
)
from django.core.cache import cache
import random
from .tasks import send_otp_sms

# complete profile view (this is when user account is created and user want to complete his/her  profile)
class CreateCustomUserView(CreateAPIView):
    """
    Register (signup) View For CustomUser
    """

    permission_classes = [IsAuthenticated]
    queryset = CustomUser.objects.all()
    serializer_class = AccountsSerializer


# Editing personal information view (this is when user want to edit his/her infomation)
class UpdateCustomUSerView(UpdateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = CustomUser.objects.all()
    serializer_class = AccountsSerializer


def generate_otp():
    return str(random.randint(100000, 999999))

# sign_in --->otp (using celey and task.py)
class SigInOTPView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = SignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone_number = serializer.validated_data['phone_number']

        otp = generate_otp()

        # Save OTP in Redis (expires in 5 minutes)
        cache.set(f"otp_{phone_number}", otp, timeout=300)

        # Send via Celery task with Kavenegar
        send_otp_sms.delay(phone_number, otp)

        return Response({"message": "OTP sent via SMS"}, status=200)

class VerifyOTPView(APIView):
    def post(self, request):
        phone = request.data.get('phone_number')
        otp = request.data.get('otp')

        cached_otp = cache.get(f"otp_{phone}")

        if not cached_otp:
            return Response({"error": "OTP expired or invalid."}, status=400)

        if cached_otp != otp:
            return Response({"error": "Invalid OTP."}, status=400)

        cache.delete(f"otp_{phone}")  # Cleanup
        return Response({"message": "OTP verified successfully"}, status=200)



# sign_in --->password (any user can sign in with password)
class SignInWithPasswordView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serialzer = SignInSerializer(data=request.data, context={"request": request})
        serialzer.is_valid(raise_exception=True)
        user = serialzer.validated_data["user"]

        refresh = RefreshToken.for_user(user)

        return Response(
            {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
                "user": {
                    "id": user.id,
                    "phone_number": user.phone_number,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                },
            }
        )

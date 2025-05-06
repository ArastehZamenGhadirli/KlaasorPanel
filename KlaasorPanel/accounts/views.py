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
    IsFinacialTeam,
    IsMentor,
    IsNormal,
    IsRegisterSupport,
    IsTeacherOrMentor,
    IsTicketSupport,
)


# complete profile view (this is when user account is created and user want to complete his/her  profile)
class CreateCustomUserView(CreateAPIView):
    """
    Register (signup) View For CustomUser
    """

    permission_classes = [IsAuthenticated]
    queryset = CustomUser.all()
    serializer_class = AccountsSerializer


# Editing personal information view (this is when user want to edit his/her infomation)
class UpdateCustomUSerView(UpdateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = CustomUser.all()
    serializer_class = AccountsSerializer


# sign_in --->otp (using celey and task.py)
class SigInOTPView(APIView):
    pass


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

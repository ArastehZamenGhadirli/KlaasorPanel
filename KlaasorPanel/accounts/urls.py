from django.urls import path
from accounts.views import (
    CreateCustomUserView,
    UpdateCustomUSerView,
    SigInOTPView,
    SignInWithPasswordView,
)


urlpatterns = [
    path('UpdateProfile/<int:pk>' , UpdateCustomUSerView.as_view()),
    path('CompleteInformation/<int:pk>' , CreateCustomUserView.as_view()),
    path('auth/SignInPassword/' , SignInWithPasswordView.as_view())
]

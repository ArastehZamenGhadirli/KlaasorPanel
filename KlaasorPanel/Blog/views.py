from django.shortcuts import render
from .models import BlogCategory, BlogPost
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
from .serializers import (
    BlogCategorySerializer,
    BlogPostSerializer,
    BlogPostCreateUpdateSerializer,
)
from rest_framework import filters
from rest_framework.permissions import (
    IsAuthenticated,
    IsAdminUser,
    IsAuthenticatedOrReadOnly,
    AllowAny,
)


class BlogCategoryListView(ListAPIView):
    """
    Public: Lists all blog categories.
    """

    queryset = BlogCategory.objects.all()
    serializer_class = BlogCategorySerializer
    permission_classes = [AllowAny]


class BlogCategoryCreateView(CreateAPIView):
    """
    Only Support team  can create a new blog category.
    """
    queryset = BlogCategory.objects.all()
    serializer_class = BlogCategorySerializer
    permission_classes = [IsRegisterSupport]


class BlogPostListView(ListAPIView):
    """
    Public: Lists all published blog posts with search
    """

    queryset = BlogPost.objects.filter(status=BlogPost.Status.PUBLISHED)
    serializer_class = BlogPostSerializer
    permission_classes = [AllowAny]
    filter_backends = [filters.SearchFilter]
    search_fields = ["title", "content"]


class BlogPostDetailView(RetrieveAPIView):
    """
    Public: Retrieve the details of a single published blog post.
    """

    queryset = BlogPost.objects.filter(status=BlogPost.Status.PUBLISHED)
    serializer_class = BlogPostSerializer
    permission_classes = [AllowAny]


class BlogPostUpdateView(UpdateAPIView):
    """
    Only the REGISTER team can update blog posts.
    """

    queryset = BlogPost.objects.all()
    serializer_class = BlogPostCreateUpdateSerializer
    permission_classes = [IsRegisterSupport | IsTicketSupport]


class BlogPostDeleteView(DestroyAPIView):
    """
    Only the TICKET team can delete blog posts.
    """

    queryset = BlogPost.objects.all()
    serializer_class = BlogPostCreateUpdateSerializer
    permission_classes = [IsTicketSupport | IsRegisterSupport]

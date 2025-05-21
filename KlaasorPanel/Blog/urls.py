from django.urls import path
from .views import (
    BlogCategoryListView,
    BlogCategoryCreateView,
    BlogPostListView,
    BlogPostDetailView,
    BlogPostUpdateView,
    BlogPostDeleteView
)

urlpatterns = [
    # Blog Categories
    path('categories/', BlogCategoryListView.as_view(), name='blog-category-list'),
    path('categories/create/', BlogCategoryCreateView.as_view(), name='blog-category-create'),
    
    # Blog Posts
    path('posts/', BlogPostListView.as_view(), name='blog-post-list'),
    path('posts/<int:pk>/', BlogPostDetailView.as_view(), name='blog-post-detail'),
    path('posts/<int:pk>/update/', BlogPostUpdateView.as_view(), name='blog-post-update'),
    path('posts/<int:pk>/delete/', BlogPostDeleteView.as_view(), name='blog-post-delete'),
]



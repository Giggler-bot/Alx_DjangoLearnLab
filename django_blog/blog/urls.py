# blog/urls.py

from django.urls import path
from .views import (
    PostListView,
    PostDetailView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
    CommentUpdateView,
    CommentDeleteView,
    register,
    profile,
    search,
    tagged,
)
from django.contrib.auth import views as auth_views

urlpatterns = [
    # Blog Post Management URLs
    path('', PostListView.as_view(), name='post_list'),
    path('post/new/', PostCreateView.as_view(), name='post_create'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('post/<int:pk>/edit/', PostUpdateView.as_view(), name='post_update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post_delete'),

    # User Authentication URLs
    path('register/', register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='registration/logout.html'), name='logout'),
    path('profile/', profile, name='profile'),

    # Comment Management URLs
    path('comment/<int:pk>/edit/', CommentUpdateView.as_view(), name='comment_update'),
    path('comment/<int:pk>/delete/', CommentDeleteView.as_view(), name='comment_delete'),

    # Tagging and Search URLs
    path('search/', search, name='search'),
    path('tags/<slug:slug>/', tagged, name='tagged_posts'),
]

["post/<int:pk>/update/"]
["tags/<slug:tag_slug>/", "PostByTagListView.as_view()"]
["comment/<int:pk>/update/", "post/<int:pk>/comments/new/"]
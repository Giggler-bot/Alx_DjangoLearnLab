from rest_framework import viewsets, permissions, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from rest_framework import generics
from django.shortcuts import get_object_or_404
from .models import Post, Comment, Like
from .serializers import PostSerializer, PostListSerializer, CommentSerializer, LikeSerializer
from notifications.utils import create_notification

class IsAuthorOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow authors to edit their own posts/comments.
    """
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed for any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Write permissions are only allowed to the author of the object.
        return obj.author == request.user

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    permission_classes = [permissions.IsAuthenticated, IsAuthorOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['author']
    search_fields = ['title', 'content']
    ordering_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']

    def get_serializer_class(self):
        if self.action == 'list':
            return PostListSerializer
        return PostSerializer

    def perform_create(self, serializer):
        # Create comment and notification
        comment = serializer.save(author=self.request.user)
        # Create notification for post author
        create_notification(
            recipient=comment.post.author,
            actor=self.request.user,
            verb='commented',
            target_object=comment.post
        )

class FeedView(generics.ListAPIView):
    """
    Get feed of posts from users that the current user follows
    """
    serializer_class = PostListSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['created_at']
    ordering = ['-created_at']

    def get_queryset(self):
        user = self.request.user
        # Get posts from users that the current user follows
        following_users = user.following.all()
        if following_users.exists():
            return Post.objects.filter(
                author__in=following_users
            ).select_related('author').prefetch_related('comments')
        else:
            # Return empty queryset if not following anyone
            return Post.objects.none()

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if not queryset.exists():
            return Response({
                'count': 0,
                'next': None,
                'previous': None,
                'results': [],
                'message': 'No posts in your feed. Start following users to see their posts here!'
            })
        return super().list(request, *args, **kwargs)

    @action(detail=True, methods=['get'])
    def comments(self, request, pk=None):
        """Get all comments for a specific post"""
        post = self.get_object()
        comments = post.comments.all()
        serializer = CommentSerializer(comments, many=True, context={'request': request})
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def like(self, request, pk=None):
        """Like a post"""
        post = self.get_object()
        like, created = Like.objects.get_or_create(user=request.user, post=post)
        
        if created:
            # Create notification for post author
            create_notification(
                recipient=post.author,
                actor=request.user,
                verb='liked',
                target_object=post
            )
            return Response({
                'message': 'Post liked successfully',
                'liked': True
            }, status=status.HTTP_201_CREATED)
        else:
            return Response({
                'message': 'You have already liked this post',
                'liked': True
            }, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def unlike(self, request, pk=None):
        """Unlike a post"""
        post = self.get_object()
        try:
            like = Like.objects.get(user=request.user, post=post)
            like.delete()
            return Response({
                'message': 'Post unliked successfully',
                'liked': False
            }, status=status.HTTP_200_OK)
        except Like.DoesNotExist:
            return Response({
                'message': 'You have not liked this post',
                'liked': False
            }, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['get'])
    def likes(self, request, pk=None):
        """Get all likes for a specific post"""
        post = self.get_object()
        likes = post.likes.all()
        serializer = LikeSerializer(likes, many=True, context={'request': request})
        return Response(serializer.data)

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated, IsAuthorOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['post', 'author']
    ordering_fields = ['created_at', 'updated_at']
    ordering = ['created_at']

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
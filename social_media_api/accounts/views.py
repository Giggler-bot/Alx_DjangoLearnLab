from rest_framework import status, generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from .models import CustomUser
from .serializers import UserRegistrationSerializer, UserLoginSerializer, UserSerializer, TokenSerializer, UserFollowSerializer
from notifications.utils import create_notification

User = get_user_model()

@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    serializer = UserRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        # Ensure token is created (should already be created in serializer)
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user': UserSerializer(user).data
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def login_user(request):
    serializer = UserLoginSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user': UserSerializer(user).data
        })
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserProfileView(generics.RetrieveUpdateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_token(request):
    """Retrieve user's authentication token"""
    token, created = Token.objects.get_or_create(user=request.user)
    return Response({
        'token': token.key,
        'user': UserSerializer(request.user).data
    })

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def follow_user(request, user_id):
    """Follow a user"""
    try:
        user_to_follow = User.objects.get(id=user_id)
        if user_to_follow == request.user:
            return Response(
                {'error': 'You cannot follow yourself'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Add to following and create notification
        request.user.following.add(user_to_follow)
        create_notification(
            recipient=user_to_follow,
            actor=request.user,
            verb='followed',
            target_object=user_to_follow
        )
        
        return Response({
            'message': f'You are now following {user_to_follow.username}',
            'user': UserFollowSerializer(user_to_follow).data
        }, status=status.HTTP_200_OK)
        
    except User.DoesNotExist:
        return Response(
            {'error': 'User not found'}, 
            status=status.HTTP_404_NOT_FOUND
        )

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def unfollow_user(request, user_id):
    """Unfollow a user"""
    try:
        user_to_unfollow = User.objects.get(id=user_id)
        if user_to_unfollow == request.user:
            return Response(
                {'error': 'You cannot unfollow yourself'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        request.user.following.remove(user_to_unfollow)
        return Response({
            'message': f'You have unfollowed {user_to_unfollow.username}',
            'user': UserFollowSerializer(user_to_unfollow).data
        }, status=status.HTTP_200_OK)
        
    except User.DoesNotExist:
        return Response(
            {'error': 'User not found'}, 
            status=status.HTTP_404_NOT_FOUND
        )

class FollowingListView(generics.ListAPIView):
    """List users that the current user is following"""
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.request.user.following.all()

class FollowersListView(generics.ListAPIView):
    """List users who follow the current user"""
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.request.user.followers.all()
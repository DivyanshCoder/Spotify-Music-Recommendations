from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.throttling import UserRateThrottle
from django.core.cache import cache
from django.contrib.auth import get_user_model
from .models import Recommendation
from .serializers import RecommendationSerializer
from .tasks import fetch_spotify_recommendations

User = get_user_model()


class RefreshRateThrottle(UserRateThrottle):
    rate = '5/hour'


class RefreshRecommendationsView(APIView):
    """POST /recommendations/{user_id}/refresh/ - Trigger async refresh"""
    permission_classes = [IsAuthenticated]
    throttle_classes = [RefreshRateThrottle]
    
    def post(self, request, user_id):
        # Check if user is accessing their own data or is admin
        if request.user.id != user_id and not request.user.is_staff:
            return Response(
                {'error': 'You can only refresh your own recommendations'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response(
                {'error': 'User not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Trigger async task
        task = fetch_spotify_recommendations.delay(user_id)
        
        return Response({
            'message': 'Recommendation refresh triggered',
            'task_id': task.id,
            'user_id': user_id
        }, status=status.HTTP_202_ACCEPTED)


class GetRecommendationsView(APIView):
    """GET /recommendations/{user_id}/ - Get cached recommendations"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request, user_id):
        # Check if user is accessing their own data or is admin
        if request.user.id != user_id and not request.user.is_staff:
            return Response(
                {'error': 'You can only view your own recommendations'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response(
                {'error': 'User not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Try cache first
        cache_key = f'recommendations_user_{user_id}'
        cached_recs = cache.get(cache_key)
        
        if cached_recs:
            serializer = RecommendationSerializer(cached_recs, many=True)
            return Response({
                'user_id': user_id,
                'source': 'cache',
                'count': len(cached_recs),
                'recommendations': serializer.data
            })
        
        # Fallback to database
        recommendations = Recommendation.objects.filter(user=user)[:50]
        
        if not recommendations.exists():
            return Response({
                'message': 'No recommendations found. Trigger a refresh first.',
                'user_id': user_id,
                'count': 0,
                'recommendations': []
            }, status=status.HTTP_200_OK)
        
        serializer = RecommendationSerializer(recommendations, many=True)
        
        # Cache for future requests
        cache.set(cache_key, list(recommendations), timeout=3600)
        
        return Response({
            'user_id': user_id,
            'source': 'database',
            'count': recommendations.count(),
            'recommendations': serializer.data
        })


class MyRecommendationsView(APIView):
    """GET /recommendations/me/ - Get current user's recommendations"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        user_id = request.user.id
        
        # Try cache first
        cache_key = f'recommendations_user_{user_id}'
        cached_recs = cache.get(cache_key)
        
        if cached_recs:
            serializer = RecommendationSerializer(cached_recs, many=True)
            return Response({
                'user_id': user_id,
                'source': 'cache',
                'count': len(cached_recs),
                'recommendations': serializer.data
            })
        
        # Fallback to database
        recommendations = Recommendation.objects.filter(user=request.user)[:50]
        
        if not recommendations.exists():
            return Response({
                'message': 'No recommendations found. Trigger a refresh first.',
                'user_id': user_id,
                'count': 0,
                'recommendations': []
            }, status=status.HTTP_200_OK)
        
        serializer = RecommendationSerializer(recommendations, many=True)
        
        # Cache for future requests
        cache.set(cache_key, list(recommendations), timeout=3600)
        
        return Response({
            'user_id': user_id,
            'source': 'database',
            'count': recommendations.count(),
            'recommendations': serializer.data
        })


class RefreshMyRecommendationsView(APIView):
    """POST /recommendations/me/refresh/ - Refresh current user's recommendations"""
    permission_classes = [IsAuthenticated]
    throttle_classes = [RefreshRateThrottle]
    
    def post(self, request):
        user_id = request.user.id
        
        # Trigger async task
        task = fetch_spotify_recommendations.delay(user_id)
        
        return Response({
            'message': 'Recommendation refresh triggered',
            'task_id': task.id,
            'user_id': user_id
        }, status=status.HTTP_202_ACCEPTED)

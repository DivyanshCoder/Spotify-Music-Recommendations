from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Count, Q
from django.utils import timezone
from django.contrib.auth import get_user_model
from datetime import timedelta
from .models import UserActivity
from .serializers import UserActivitySerializer
from recommendations.models import Recommendation

User = get_user_model()


class RecordActivityView(APIView):
    """POST /activity/ - Record user interaction"""
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        # Automatically set the user to the authenticated user
        data = request.data.copy()
        data['user'] = request.user.id
        
        serializer = UserActivitySerializer(data=data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AnalyticsSummaryView(APIView):
    """GET /analytics/summary/ - Overall usage stats"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        # Admin sees all stats, regular users see their own
        if request.user.is_staff:
            total_users = User.objects.count()
            total_recommendations = Recommendation.objects.count()
            total_activities = UserActivity.objects.count()
            
            activity_breakdown = UserActivity.objects.values('interaction_type').annotate(
                count=Count('id')
            )
            
            week_ago = timezone.now() - timedelta(days=7)
            recent_activities = UserActivity.objects.filter(timestamp__gte=week_ago).count()
            
            active_users = UserActivity.objects.filter(
                timestamp__gte=week_ago
            ).values('user').distinct().count()
            
            return Response({
                'total_users': total_users,
                'total_recommendations': total_recommendations,
                'total_activities': total_activities,
                'active_users_last_7_days': active_users,
                'activities_last_7_days': recent_activities,
                'activity_breakdown': list(activity_breakdown)
            })
        else:
            # Regular user sees only their stats
            user = request.user
            total_activities = UserActivity.objects.filter(user=user).count()
            
            activity_breakdown = UserActivity.objects.filter(user=user).values(
                'interaction_type'
            ).annotate(count=Count('id'))
            
            week_ago = timezone.now() - timedelta(days=7)
            recent_activities = UserActivity.objects.filter(
                user=user,
                timestamp__gte=week_ago
            ).count()
            
            return Response({
                'user_id': user.id,
                'total_activities': total_activities,
                'activities_last_7_days': recent_activities,
                'activity_breakdown': list(activity_breakdown)
            })


class TrendsView(APIView):
    """GET /analytics/trends/ - Trending genres/artists"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        week_ago = timezone.now() - timedelta(days=7)
        
        recent_activities = UserActivity.objects.filter(
            timestamp__gte=week_ago,
            interaction_type__in=['play', 'like']
        ).select_related('recommendation')
        
        artist_counts = {}
        genre_counts = {}
        
        for activity in recent_activities:
            artist = activity.recommendation.artist_name
            artist_counts[artist] = artist_counts.get(artist, 0) + 1
            
            for genre in activity.recommendation.genres:
                genre_counts[genre] = genre_counts.get(genre, 0) + 1
        
        trending_artists = sorted(
            artist_counts.items(), 
            key=lambda x: x[1], 
            reverse=True
        )[:10]
        
        trending_genres = sorted(
            genre_counts.items(), 
            key=lambda x: x[1], 
            reverse=True
        )[:10]
        
        return Response({
            'trending_artists': [
                {'name': artist, 'interactions': count} 
                for artist, count in trending_artists
            ],
            'trending_genres': [
                {'name': genre, 'interactions': count} 
                for genre, count in trending_genres
            ]
        })


class UserEngagementView(APIView):
    """GET /analytics/user/{user_id}/ - User-specific engagement"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request, user_id):
        # Users can only see their own stats unless they're admin
        if request.user.id != user_id and not request.user.is_staff:
            return Response(
                {'error': 'You can only view your own engagement stats'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response(
                {'error': 'User not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        
        total_activities = UserActivity.objects.filter(user=user).count()
        
        activity_breakdown = UserActivity.objects.filter(user=user).values(
            'interaction_type'
        ).annotate(count=Count('id'))
        
        week_ago = timezone.now() - timedelta(days=7)
        recent_activities = UserActivity.objects.filter(
            user=user, 
            timestamp__gte=week_ago
        ).count()
        
        top_tracks = UserActivity.objects.filter(user=user).values(
            'recommendation__track_name',
            'recommendation__artist_name'
        ).annotate(
            interaction_count=Count('id')
        ).order_by('-interaction_count')[:10]
        
        return Response({
            'user_id': user_id,
            'user_email': user.email,
            'total_activities': total_activities,
            'activities_last_7_days': recent_activities,
            'activity_breakdown': list(activity_breakdown),
            'top_tracks': list(top_tracks)
        })

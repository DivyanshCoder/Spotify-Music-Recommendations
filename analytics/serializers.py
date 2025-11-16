from rest_framework import serializers
from .models import UserActivity

class UserActivitySerializer(serializers.ModelSerializer):
    track_name = serializers.CharField(source='recommendation.track_name', read_only=True)
    artist_name = serializers.CharField(source='recommendation.artist_name', read_only=True)
    
    class Meta:
        model = UserActivity
        fields = [
            'id', 'user', 'recommendation', 'interaction_type', 
            'timestamp', 'metadata', 'track_name', 'artist_name'
        ]
        read_only_fields = ['id', 'timestamp']

from rest_framework import serializers
from .models import Recommendation

class RecommendationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recommendation
        fields = [
            'id', 'track_id', 'track_name', 'artist_name', 
            'album_name', 'preview_url', 'spotify_url', 
            'genres', 'popularity', 'duration_ms', 'metadata', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']

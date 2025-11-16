from celery import shared_task
from django.core.cache import cache
from django.utils import timezone
from django.contrib.auth import get_user_model
from .models import Recommendation
from .spotify_client import SpotifyClient
import logging

User = get_user_model()
logger = logging.getLogger(__name__)

@shared_task(bind=True, max_retries=3)
def fetch_spotify_recommendations(self, user_id):
    """
    Background task to fetch recommendations from Spotify API
    """
    try:
        user = User.objects.get(id=user_id)
        client = SpotifyClient()
        
        # Convert artist names to IDs and get their tracks
        seed_artists = []
        seed_tracks = []
        
        for artist_name in user.favorite_artists[:3]:
            artist_id = client.search_artist(artist_name)
            if artist_id:
                seed_artists.append(artist_id)
                # Get popular tracks from this artist
                tracks = client.get_popular_tracks_by_artist(artist_id, limit=2)
                seed_tracks.extend(tracks)
        
        # Limit to 5 seeds total (Spotify requirement)
        seed_artists = seed_artists[:2]
        seed_tracks = seed_tracks[:3]
        
        # Fallback if no seeds found
        if not seed_artists and not seed_tracks:
            # Use default popular artists
            seed_artists = [
                '4YRxDV8wJFPHPTeXepOstw',  # Coldplay
                '6eUKZXaKkcviH0Ku9w2n3V',  # Ed Sheeran
            ]
        
        # Map moods to Spotify audio features
        mood_params = _map_moods_to_features(user.moods)
        
        # Fetch recommendations from Spotify
        # Note: Not using seed_genres due to API deprecation
        spotify_data = client.get_recommendations(
            seed_artists=seed_artists,
            seed_tracks=seed_tracks,
            limit=50,
            **mood_params
        )
        
        # Clear old recommendations (keep last 100)
        old_recs = Recommendation.objects.filter(user=user).order_by('-created_at')[100:]
        old_recs.delete()
        
        # Save new recommendations
        recommendations = []
        for track in spotify_data.get('tracks', []):
            rec = Recommendation(
                user=user,
                track_id=track['id'],
                track_name=track['name'],
                artist_name=', '.join([artist['name'] for artist in track['artists']]),
                album_name=track['album']['name'],
                preview_url=track.get('preview_url'),
                spotify_url=track['external_urls']['spotify'],
                popularity=track.get('popularity', 0),
                duration_ms=track.get('duration_ms', 0),
                metadata={
                    'album_image': track['album']['images'][0]['url'] if track['album']['images'] else None,
                    'release_date': track['album'].get('release_date'),
                }
            )
            recommendations.append(rec)
        
        Recommendation.objects.bulk_create(recommendations)
        
        # Cache the recommendations
        cache_key = f'recommendations_user_{user_id}'
        cache.set(cache_key, recommendations, timeout=3600)
        
        logger.info(f"Successfully fetched {len(recommendations)} recommendations for user {user_id}")
        
        return {
            'user_id': user_id,
            'count': len(recommendations),
            'status': 'success'
        }
        
    except User.DoesNotExist:
        logger.error(f"User {user_id} not found")
        return {'error': 'User not found'}
    
    except Exception as exc:
        logger.error(f"Error fetching recommendations for user {user_id}: {str(exc)}")
        raise self.retry(exc=exc, countdown=60)



@shared_task
def refresh_all_users_recommendations():
    """
    Periodic task to refresh recommendations for all users
    """
    users = User.objects.filter(is_active=True)
    
    for user in users:
        fetch_spotify_recommendations.delay(user.id)
    
    logger.info(f"Triggered recommendation refresh for {users.count()} users")
    
    return {'triggered': users.count()}


def _map_moods_to_features(moods):
    """Map user moods to Spotify audio features"""
    mood_mapping = {
        'energetic': {'min_energy': 0.7, 'min_tempo': 120},
        'calm': {'max_energy': 0.4, 'max_tempo': 100},
        'happy': {'min_valence': 0.7},
        'sad': {'max_valence': 0.3},
        'focused': {'min_instrumentalness': 0.5, 'max_speechiness': 0.3},
        'party': {'min_danceability': 0.7, 'min_energy': 0.7},
    }
    
    features = {}
    for mood in moods:
        mood_lower = mood.lower()
        if mood_lower in mood_mapping:
            features.update(mood_mapping[mood_lower])
    
    return features

import base64
import requests
from django.conf import settings
from django.core.cache import cache
import random

class SpotifyClient:
    """Client for interacting with Spotify Web API"""
    
    def __init__(self):
        self.client_id = settings.SPOTIFY_CLIENT_ID
        self.client_secret = settings.SPOTIFY_CLIENT_SECRET
        self.token_url = settings.SPOTIFY_TOKEN_URL
        self.api_base_url = settings.SPOTIFY_API_BASE_URL
        
    def _get_access_token(self):
        """Get cached access token or request new one"""
        token = cache.get('spotify_access_token')
        
        if token:
            return token
        
        # TODO: Replace with your SPOTIFY_CLIENT_ID and SPOTIFY_CLIENT_SECRET
        credentials = f"{self.client_id}:{self.client_secret}"
        credentials_b64 = base64.b64encode(credentials.encode()).decode()
        
        headers = {
            'Authorization': f'Basic {credentials_b64}',
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        
        data = {'grant_type': 'client_credentials'}
        
        response = requests.post(self.token_url, headers=headers, data=data)
        response.raise_for_status()
        
        token_data = response.json()
        token = token_data['access_token']
        expires_in = token_data.get('expires_in', 3600)
        
        cache.set('spotify_access_token', token, timeout=expires_in - 60)
        
        return token
    
    def _make_request(self, endpoint, params=None):
        """Make authenticated request to Spotify API"""
        token = self._get_access_token()
        
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }
        
        url = f"{self.api_base_url}/{endpoint}"
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        
        return response.json()
    
    def get_recommendations(self, seed_genres=None, seed_artists=None, limit=20, **kwargs):
        """
        Get track recommendations using Search endpoint
        (Original /recommendations endpoint was deprecated Nov 27, 2024)
        
        Args:
            seed_genres: List of genres to search for
            seed_artists: List of artist names or IDs
            limit: Number of tracks to return
            **kwargs: Mood parameters (not used with search, but kept for compatibility)
        """
        all_tracks = []
        
        # Strategy 1: Search by artist names
        if seed_artists:
            for artist in seed_artists[:3]:
                try:
                    # Get artist's top tracks
                    artist_id = artist if len(artist) == 22 else self.search_artist(artist)
                    if artist_id:
                        tracks = self.get_artist_top_tracks(artist_id)
                        all_tracks.extend(tracks.get('tracks', [])[:5])
                except:
                    continue
        
        # Strategy 2: Search by genre keywords
        if seed_genres and len(all_tracks) < limit:
            for genre in seed_genres[:3]:
                try:
                    search_query = f"genre:{genre}"
                    result = self.search_tracks(search_query, limit=10)
                    tracks = result.get('tracks', {}).get('items', [])
                    all_tracks.extend(tracks)
                except:
                    continue
        
        # Strategy 3: Search popular tracks if nothing else worked
        if len(all_tracks) < limit:
            try:
                popular_queries = ['top hits', 'viral tracks', 'trending music']
                query = random.choice(popular_queries)
                result = self.search_tracks(query, limit=20)
                tracks = result.get('tracks', {}).get('items', [])
                all_tracks.extend(tracks)
            except:
                pass
        
        # Remove duplicates and limit
        unique_tracks = []
        seen_ids = set()
        for track in all_tracks:
            if track['id'] not in seen_ids:
                unique_tracks.append(track)
                seen_ids.add(track['id'])
            if len(unique_tracks) >= limit:
                break
        
        return {'tracks': unique_tracks[:limit]}
    
    def search_artist(self, artist_name):
        """Search for artist by name and return artist ID"""
        params = {
            'q': artist_name,
            'type': 'artist',
            'limit': 1
        }
        
        result = self._make_request('search', params=params)
        
        if result['artists']['items']:
            return result['artists']['items'][0]['id']
        
        return None
    
    def search_tracks(self, query, limit=20):
        """Search for tracks by query"""
        params = {
            'q': query,
            'type': 'track',
            'limit': limit,
            'market': 'US'
        }
        return self._make_request('search', params=params)
    
    def get_artist_top_tracks(self, artist_id, market='US'):
        """Get artist's top tracks"""
        return self._make_request(f'artists/{artist_id}/top-tracks', params={'market': market})
    
    def get_available_genres(self):
        """Note: This endpoint is also deprecated, returning mock data"""
        return {
            'genres': [
                'pop', 'rock', 'hip-hop', 'jazz', 'classical', 
                'electronic', 'indie', 'metal', 'country', 'r-n-b'
            ]
        }

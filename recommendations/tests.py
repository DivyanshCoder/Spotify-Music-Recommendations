import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from users.models import UserProfile
from recommendations.models import Recommendation

@pytest.mark.django_db
class TestRecommendations:
    
    def setup_method(self):
        self.client = APIClient()
        self.user = UserProfile.objects.create(
            name='Test User',
            email='test@example.com',
            favorite_genres=['pop', 'rock']
        )
    
    def test_refresh_recommendations(self):
        """Test triggering recommendation refresh"""
        url = reverse('refresh-recommendations', kwargs={'user_id': self.user.id})
        response = self.client.post(url)
        
        assert response.status_code == status.HTTP_202_ACCEPTED
        assert 'task_id' in response.data
    
    def test_get_recommendations_empty(self):
        """Test getting recommendations when none exist"""
        url = reverse('get-recommendations', kwargs={'user_id': self.user.id})
        response = self.client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['count'] == 0

from django.urls import path
from .views import (
    RefreshRecommendationsView,
    GetRecommendationsView,
    MyRecommendationsView,
    RefreshMyRecommendationsView
)

urlpatterns = [
    # Current user endpoints
    path('me/', MyRecommendationsView.as_view(), name='my-recommendations'),
    path('me/refresh/', RefreshMyRecommendationsView.as_view(), name='refresh-my-recommendations'),
    
    # Specific user endpoints (admin or self)
    path('<int:user_id>/refresh/', RefreshRecommendationsView.as_view(), name='refresh-recommendations'),
    path('<int:user_id>/', GetRecommendationsView.as_view(), name='get-recommendations'),
]

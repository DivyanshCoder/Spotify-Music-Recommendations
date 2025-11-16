from django.urls import path
from .views import (
    CurrentUserView,
    UserDetailView,
    UserProfileCreateUpdateView,
    UserProfileDetailView
)

urlpatterns = [
    # New authenticated endpoints
    path('me/', CurrentUserView.as_view(), name='current-user'),
    path('<int:user_id>/', UserDetailView.as_view(), name='user-detail-auth'),
    
    # Legacy endpoints
    path('profile/', UserProfileCreateUpdateView.as_view(), name='user-create-update'),
    path('profile/<int:user_id>/', UserProfileDetailView.as_view(), name='user-profile-detail'),
]

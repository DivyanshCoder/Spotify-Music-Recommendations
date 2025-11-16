from django.urls import path
from .views import (
    RecordActivityView,
    AnalyticsSummaryView,
    TrendsView,
    UserEngagementView
)

urlpatterns = [
    path('', RecordActivityView.as_view(), name='record-activity'),
    path('summary/', AnalyticsSummaryView.as_view(), name='analytics-summary'),
    path('trends/', TrendsView.as_view(), name='analytics-trends'),
    path('user/<int:user_id>/', UserEngagementView.as_view(), name='user-engagement'),
]

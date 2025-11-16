from django.db import models
from django.contrib.auth import get_user_model
from recommendations.models import Recommendation

User = get_user_model()


class UserActivity(models.Model):
    INTERACTION_CHOICES = [
        ('play', 'Play'),
        ('like', 'Like'),
        ('skip', 'Skip'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='activities')
    recommendation = models.ForeignKey(Recommendation, on_delete=models.CASCADE, related_name='activities')
    interaction_type = models.CharField(max_length=10, choices=INTERACTION_CHOICES)
    timestamp = models.DateTimeField(auto_now_add=True)
    metadata = models.JSONField(default=dict, blank=True)

    class Meta:
        db_table = 'user_activities'
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['user', '-timestamp']),
            models.Index(fields=['interaction_type']),
        ]

    def __str__(self):
        return f"{self.user.email} - {self.interaction_type} - {self.recommendation.track_name}"

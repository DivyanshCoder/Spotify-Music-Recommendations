from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Recommendation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recommendations')
    track_id = models.CharField(max_length=255)
    track_name = models.CharField(max_length=500)
    artist_name = models.CharField(max_length=500)
    album_name = models.CharField(max_length=500, blank=True)
    preview_url = models.URLField(blank=True, null=True)
    spotify_url = models.URLField()
    genres = models.JSONField(default=list, blank=True)
    popularity = models.IntegerField(default=0)
    duration_ms = models.IntegerField(default=0)
    metadata = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'recommendations'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', '-created_at']),
            models.Index(fields=['track_id']),
        ]

    def __str__(self):
        return f"{self.track_name} by {self.artist_name} for {self.user.email}"

from django.db import models
from channels.models import Channel

class Video(models.Model):
    title = models.CharField(max_length=150)
    youtube_url = models.URLField()
    order = models.PositiveIntegerField()
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE, related_name='videos')
    description = models.TextField(blank=True)
    thumbnail_url = models.URLField(blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.channel.name})"

    class Meta:
        ordering = ['order']

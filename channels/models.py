# channels/models.py
from django.db import models
from django.contrib.auth.models import User

class Channel(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)  # <-- add this

    def __str__(self):
        return self.name

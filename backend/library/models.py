from django.db import models
from user.models import User
from song.models import Song

class Library(models.Model):
    user  = models.OneToOneField(User, on_delete=models.CASCADE, related_name="library")
    songs = models.ManyToManyField(Song, blank=True, related_name="libraries")
 
    def __str__(self):
        return f"{self.user.name}'s Library"

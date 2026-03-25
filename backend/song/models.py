from django.db import models

# Create your models here.
class Song(models.Model):
    title = models.CharField(max_length=256)
    occasion = models.CharField(max_length=64)
    mood_tone =  models.CharField(max_length=64)
    genre =  models.CharField(max_length=64)
    singer_voice = models.CharField(max_length=256)
    meaning = models.CharField(max_length=256)
    song_durations = models.TimeField()


    def __str__(self):
        return self.title
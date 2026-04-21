from django.db import models

# Create your models here.
class Song(models.Model):
    STRATEGY_CHOICES = [
        ('mock', 'Mock'),
        ('suno', 'Suno'),
    ]
    
    SINGER_VOICE_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
    ]
    
    GEN_STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('GENERATING', 'Generating'),
        ('SUCCESS', 'Success'),
        ('FAILED', 'Failed'),
    ]
    
    title = models.CharField(max_length=256)
    occasion = models.CharField(max_length=64)
    mood_tone =  models.CharField(max_length=64)
    genre =  models.CharField(max_length=64)
    singer_voice = models.CharField(max_length=10, choices=SINGER_VOICE_CHOICES, default='male')
    meaning = models.CharField(max_length=256)
    song_durations = models.TimeField()

    strategy = models.CharField(max_length=10, choices=STRATEGY_CHOICES, default='mock')
    song_path = models.CharField(max_length=512, blank=True, null=True, help_text="Folder path where the song is stored (e.g., storage/song/song_id)")
    generation_status = models.CharField(max_length=20, choices=GEN_STATUS_CHOICES, default='PENDING')
    
    # Task and file management
    task_id = models.CharField(max_length=256, blank=True, null=True, help_text="External API task ID (e.g., Suno API task ID)")
    audio_url = models.CharField(max_length=512, blank=True, null=True, help_text="Path or URL to the generated audio file")

    def __str__(self):
        return self.title
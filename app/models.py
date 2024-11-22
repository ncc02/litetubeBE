from django.db import models

class Video(models.Model):
    VIDEO_TYPES = [
        ('MUSIC', 'Music'),
        ('ANIME', 'Anime'),
    ]
    title = models.CharField(max_length=200)
    description = models.TextField()
    video_file = models.FileField(upload_to='videos/')
    created_at = models.DateTimeField(auto_now_add=True)
    type = models.CharField(max_length=10, choices=VIDEO_TYPES, default='MUSIC') 
    
    def __str__(self):
        return f"{self.title} ({self.get_type_display()})"

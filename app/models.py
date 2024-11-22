from django.db import models
import cv2
import os
from django.core.files.base import ContentFile

class Video(models.Model):
    VIDEO_TYPES = [
        ('MUSIC', 'Music'),
        ('ANIME', 'Anime'),
        ('GAME', 'Game'),
        ('OTHER', 'Other'),
    ]
    title = models.CharField(max_length=200)
    description = models.TextField()
    video_file = models.FileField(upload_to='videos/')
    thumbnail = models.ImageField(upload_to='thumbnails/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    type = models.CharField(max_length=10, choices=VIDEO_TYPES, default='MUSIC') 

    def __str__(self):
        return f"{self.title} ({self.get_type_display()})"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # Lưu đối tượng trước

        if self.video_file and not self.thumbnail:
            video_path = self.video_file.path
            cap = cv2.VideoCapture(video_path)
            success, frame = cap.read()  # Đọc frame đầu tiên
            if success:
                # Lưu frame dưới dạng file tạm thời
                from PIL import Image
                from io import BytesIO
                image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
                temp_thumb = BytesIO()
                image.save(temp_thumb, format="JPEG")
                temp_thumb.seek(0)
                
                # Lưu vào trường thumbnail
                self.thumbnail.save(
                    os.path.basename(video_path).replace(".mp4", ".jpg"),
                    ContentFile(temp_thumb.read()),
                    save=False
                )
                temp_thumb.close()
            cap.release()
            super().save(*args, **kwargs)  # Lưu lại với thumbnail

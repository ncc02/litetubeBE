from rest_framework.viewsets import ModelViewSet
from .models import Video
from .serializers import VideoSerializer

class VideoViewSet(ModelViewSet):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer

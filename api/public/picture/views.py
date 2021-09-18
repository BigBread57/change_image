from PIL import Image
from rest_framework import generics

from api.public.picture.serializers import PictureListCreateSerializer
from picture.models import Picture


class PictureListCreateApiView(generics.ListCreateAPIView):
    """
    Предтавление для получения списка картинок и создания картинки
    """

    queryset = Picture.objects.all()
    serializer_class = PictureListCreateSerializer

    def perform_create(self, serializer):
        image = Image.open(serializer.validated_data.get('picture'))
        serializer.save(width=image.size[0], height=image.size[1])


class PictureRetrieveDestroyApiView(generics.RetrieveDestroyAPIView):
    """
    Предтавление для получения конкретной картинки и ее удаления
    """

    queryset = Picture.objects.all()
    serializer_class = PictureListCreateSerializer
    lookup_fields = ['id']

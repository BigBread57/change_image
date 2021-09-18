from io import BytesIO

import requests

from PIL import Image
from django.core.files.base import ContentFile
from rest_framework import generics, status
from rest_framework.response import Response

from api.public.picture.serializers import PictureListCreateSerializer
from picture.models import Picture


class PictureListCreateApiView(generics.ListCreateAPIView):
    """
    Предтавление для получения списка картинок и создания картинки
    """

    queryset = Picture.objects.all()
    serializer_class = PictureListCreateSerializer

    def perform_create(self, serializer):
        print('sdfsdfsfdsdfsdfsdfsdfsdf')
        print(self)
        print(serializer)

        image = Image.open(serializer.validated_data.get('picture'))
        serializer.save(width=image.size[0], height=image.size[1])

    def create(self, request, *args, **kwargs):
        url = request.data.get('url')

        name_picture = url.split('/')[-1:][0]

        if request.data.get('url'):
            url = request.data.get('url')
            try:
                resp = requests.get(url, stream=True).raw
            except requests.exceptions.RequestException as e:
                return Response(status=status.HTTP_204_NO_CONTENT, data={
                    'message': 'По заданному адресу ничего нет'})

            try:
                img = Image.open(resp)
            except IOError:
                return Response(status=status.HTTP_204_NO_CONTENT, data={
                    'message': 'Невозможно открыть изображение'})

            img.save(name_picture)
            width = img.size[0]
            height = img.size[1]

            with BytesIO() as buf:
                img.save(buf, 'jpeg')
                image_bytes = buf.getvalue()

            django_file = ContentFile(image_bytes)
            new_picture = Picture.objects.create(name=name_picture, width=width, height=height)
            new_picture.picture.save(name_picture, django_file)
            new_picture.save()

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class PictureRetrieveDestroyApiView(generics.RetrieveDestroyAPIView):
    """
    Предтавление для получения конкретной картинки и ее удаления
    """

    queryset = Picture.objects.all()
    serializer_class = PictureListCreateSerializer
    lookup_fields = ['id']

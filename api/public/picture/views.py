from io import BytesIO

import requests

from PIL import Image
from django.core.files.base import ContentFile
from django.db import IntegrityError
from rest_framework import generics, status, exceptions
from rest_framework.response import Response

from api.public.picture.serializers import PictureListCreateSerializer, PictureRetrieveDestroySerializer, \
    PictureResizeSerializer
from picture.models import Picture


class PictureListCreateApiView(generics.ListCreateAPIView):
    """
    Предтавление для получения списка картинок и создания картинки
    """

    queryset = Picture.objects.all().order_by('-id')
    serializer_class = PictureListCreateSerializer

    def perform_create(self, serializer):
        url = serializer.validated_data.get('url')
        if not url:
            name_picture = serializer.validated_data.get('picture')
            picture = Image.open(name_picture)
            serializer.save(name=name_picture, width=picture.width, height=picture.height)
        serializer.save()

    def create(self, request, *args, **kwargs):
        url = request.data.get('url')
        picture = request.data.get('picture')

        if url:
            name_picture = url.split('/')[-1:][0]
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

            # with BytesIO() as buf:
            #     img.save(buf, 'jpeg')
            #     picture_bytes = buf.getvalue()
            # django_file = ContentFile(picture_bytes)

            # new_picture = Picture(name=name_picture, width=img.width, height=img.height)
            # new_picture.picture.save(name_picture, django_file)
            # print(new_picture.id)

            data_for_serializer = {'name': name_picture,
                                   'url': url,
                                   'width': img.width,
                                   'height': img.height,
                                   'parent_picture': 'null'}

        if picture:
            data_for_serializer = request.data

        if picture and url:
            data_for_serializer = request.data

        serializer = self.get_serializer(data=data_for_serializer)
        print('1')
        serializer.is_valid(raise_exception=True)
        print('2')
        self.perform_create(serializer)
        print('3')
        headers = self.get_success_headers(serializer.data)
        print('4')
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class PictureRetrieveDestroyApiView(generics.RetrieveDestroyAPIView):
    """
    Предтавление для получения конкретной картинки и ее удаления
    """

    queryset = Picture.objects.all()
    serializer_class = PictureRetrieveDestroySerializer
    lookup_fields = ['id']


class PictureResizeApiView(generics.CreateAPIView):
    queryset = Picture.objects.all()
    serializer_class = PictureResizeSerializer

    def get_queryset(self):
        return super().get_queryset().filter(id=self.kwargs.get('pk'))

    def perform_create(self, serializer):
        new_name_picture = '_'
        picture = Picture.objects.get(id=self.kwargs.get('pk'))

        if serializer.validated_data.get('width') is None and serializer.validated_data.get('height') is None:
            raise exceptions.ValidationError(detail={
                'message': 'Необходимо ввести не менее одного значения'})

        if serializer.validated_data.get('width'):
            width = serializer.validated_data.get('width')
            new_name_picture = f'{new_name_picture}{width}'
        else:
            width = picture.width
            new_name_picture = f'{new_name_picture}_0'

        if serializer.validated_data.get('height'):
            height = serializer.validated_data.get('height')
            new_name_picture = f'{new_name_picture}{height}'
        else:
            height = picture.height
            new_name_picture = f'{new_name_picture}_0'

        try:
            parent_picture = Image.open(picture.picture)
        except IOError:
            return Response(status=status.HTTP_204_NO_CONTENT, data={
                'message': 'Невозможно найти изображение'})
        format_children_picture = picture.name.split('.')[-1:][0]
        name_children_picture = f'{picture.name}{new_name_picture}.{format_children_picture}'
        children_picture = parent_picture.resize((width, height), Image.ANTIALIAS)
        children_picture.save(name_children_picture)

        img = Image.open(name_children_picture)
        with BytesIO() as buf:
            img.save(buf, 'jpeg')
            picture_bytes = buf.getvalue()
        django_file = ContentFile(picture_bytes)

        serializer.save(name=name_children_picture,
                        url=picture.url,
                        picture=(name_children_picture, django_file),
                        width=width,
                        height=height,
                        parent_picture=picture)

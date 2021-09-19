from io import BytesIO

import requests

from PIL import Image
from django.core.files.base import ContentFile
from rest_framework import generics, status, exceptions
from rest_framework.response import Response

from api.public.picture.serializers import PictureRetrieveDestroySerializer, PictureResizeSerializer, \
    PictureListCreateSerializer
from picture.models import Picture, PictureInfo


class PictureListCreateApiView(generics.ListCreateAPIView):
    """
    Предтавление для получения списка картинок и создания картинки
    """

    queryset = Picture.objects.all()
    serializer_class = PictureListCreateSerializer

    def create(self, request, *args, **kwargs):
        url = request.data.get('url')
        picture = request.data.get('picture')

        if not url and not picture:
            raise exceptions.ValidationError(detail={'message': 'Необходимо ввести любой из параметров'})

        # Если был передан url
        if url and not picture:
            name_picture = url.split('/')[-1:][0]
            # Проверяем есть ли по заданному url картинки
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

            # Создаем объект картинки и заносим информацию в БД.
            # Преобразуем наше изображение в строковое содержимое байтов.
            with BytesIO() as buf:
                img.save(buf, 'jpeg')
                picture_bytes = buf.getvalue()
            django_file = ContentFile(picture_bytes)

            new_picture = Picture(url=url)
            new_picture.picture.save(name_picture, django_file)
            new_picture.save()

            # Представляем данные для сериализатора и передаем id созданного объекта
            # upload_from_url - необходимо для понимания того, что загрузка произошла через url
            # при передаче и url и файла будет передана только картинка
            data_for_serializer = {'csrfmiddlewaretoken': request.data.get('csrfmiddlewaretoken'),
                                   'url': url,
                                   'picture': new_picture.picture,
                                   'picture_id': new_picture.id,
                                   'upload_from_url': True}

        # Если был передана картинка
        if picture:
            data_for_serializer = request.data

        serializer = self.get_serializer(data=data_for_serializer)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
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

    def create(self, request, *args, **kwargs):
        new_name_picture = '_'
        obj_picture = PictureInfo.objects.get(picture_id=self.kwargs.get('pk'))
        width = request.data.get('width')
        height = request.data.get('height')

        if width == '' and height == '':
            raise exceptions.ValidationError(detail={
                'message': 'Необходимо ввести не менее одного значения'})

        if width:
            new_name_picture = f'{new_name_picture}{width}'
        else:
            width = obj_picture.width
            new_name_picture = f'{new_name_picture}_0'

        if height:
            new_name_picture = f'{new_name_picture}{height}'
        else:
            height = obj_picture.height
            new_name_picture = f'{new_name_picture}_0'

        try:
            parent_picture = Image.open(obj_picture.picture.picture)
        except IOError:
            return Response(status=status.HTTP_204_NO_CONTENT, data={
                'message': 'Невозможно найти изображение'})

        data_for_serializer = {'csrfmiddlewaretoken': request.data.get('csrfmiddlewaretoken'),
                               'width': width, 'height': height}
        serializer = self.get_serializer(data=data_for_serializer)
        serializer.is_valid(raise_exception=True)

        # Формируем новое название измененного файла
        format_children_picture = obj_picture.name.split('.')[-1:][0]
        name_children_picture = f'{obj_picture.name}{new_name_picture}.{format_children_picture}'

        children_picture = parent_picture.resize((int(width), int(height)), Image.ANTIALIAS)
        children_picture.save(name_children_picture)

        img = Image.open(name_children_picture)
        with BytesIO() as buf:
            img.save(buf, 'png')
            picture_bytes = buf.getvalue()
        django_file = ContentFile(picture_bytes)

        children_picture = Picture()
        children_picture.picture.save(name_children_picture, django_file)
        children_picture.save()
        PictureInfo.objects.create(name=name_children_picture, picture=children_picture,
                                   width=width, height=height, parent_picture=obj_picture.picture)
        serializer = self.get_serializer(data={'csrfmiddlewaretoken': request.data.get('csrfmiddlewaretoken'),
                                               'width': width, 'height': height,
                                               'children_picture_id': children_picture})
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

from io import BytesIO

import requests

from PIL import Image
from django.core.files.base import ContentFile
from django.db import models


class Picture(models.Model):
    """
    Модель изображений
    """

    name = models.CharField('Название изображения', max_length=100)
    url = models.CharField('URL изображения', max_length=1000, null=True)
    picture = models.ImageField(blank=True)
    width = models.PositiveSmallIntegerField('Ширина изображения', blank=True, null=True)
    height = models.PositiveSmallIntegerField('Высота изображения', blank=True, null=True)
    parent_picture = models.ForeignKey('picture.Picture', on_delete=models.SET_NULL,
                                       verbose_name='Родительская картинка', related_name='pictures', null=True)

    class Meta:
        verbose_name = 'Картинка'
        verbose_name_plural = 'Картинки'

    def __str__(self):
        return self.name

    # def save(self, force_insert=False, force_update=False, using=None,
    #          update_fields=None):
    #     if self.url:
    #         img = Image.open(requests.get(self.url, stream=True).raw)
    #         name_picture = self.url.split('/')[-1:][0]
    #         with BytesIO() as buf:
    #             img.save(buf, 'jpeg')
    #             picture_bytes = buf.getvalue()
    #         django_file = ContentFile(picture_bytes)
    #         self.picture.save(name_picture, django_file)
    #         self.save()


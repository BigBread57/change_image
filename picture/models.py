from django.db import models


class Picture(models.Model):
    """
    Модель изображений
    """

    name = models.CharField('Название изображения', max_length=100)
    url = models.SlugField('URL изображения', null=True)
    picture = models.ImageField()
    width = models.PositiveSmallIntegerField('Ширина изображения', blank=True, null=True)
    height = models.PositiveSmallIntegerField('Высота изображения', blank=True, null=True)
    parent_picture = models.OneToOneField('picture.Picture', on_delete=models.SET_NULL,
                                          verbose_name='Родительская картинка', related_name='pictures', null=True)

    class Meta:
        verbose_name = 'Картинка'
        verbose_name_plural = 'Картинки'

    def __str__(self):
        return self.name

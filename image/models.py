from django.db import models


class Picture(models.Model):
    """
    Модель изображений
    """

    name = models.CharField('Название изображения', max_length=100)
    url = models.SlugField('URL изображения')
    picture = models.ImageField()
    width = models.FloatField('Ширина изображения')
    height = models.FloatField('Высота изображения')
    parent_picture = models.OneToOneField('image.Picture', on_delete=models.SET_NULL,
                                          verbose_name='Родительская картинка', related_name='pictures')

    class Meta:
        verbose_name = 'Картинка'
        verbose_name_plural = 'Картинки'

    def __str__(self):
        return self.name

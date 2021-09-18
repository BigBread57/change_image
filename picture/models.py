from django.db import models


class Picture(models.Model):
    """
    Модель изображения
    """

    url = models.CharField('URL изображения', max_length=1000, null=True)
    picture = models.ImageField(blank=True)

    class Meta:
        verbose_name = 'Картинка'
        verbose_name_plural = 'Картинки'

    def __str__(self):
        return str(self.picture)


class PictureInfo(models.Model):
    """
    Модель информации об изображении
    """

    name = models.CharField('Название изображения', max_length=100)
    picture = models.OneToOneField(Picture, on_delete=models.CASCADE,
                                   verbose_name='Картинка', related_name='picture_information', null=True)
    width = models.PositiveSmallIntegerField('Ширина изображения', blank=True, null=True)
    height = models.PositiveSmallIntegerField('Высота изображения', blank=True, null=True)
    parent_picture = models.ForeignKey(Picture, on_delete=models.SET_NULL, verbose_name='Родительская картинка',
                                       related_name='picture_information_parent', null=True)

    class Meta:
        verbose_name = 'Информация о картинке'
        verbose_name_plural = 'Информация о картинках'

    def __str__(self):
        return self.name


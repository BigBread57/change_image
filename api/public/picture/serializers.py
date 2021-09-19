from PIL import Image
from django.core.validators import MinValueValidator, MaxValueValidator
from rest_framework import serializers

from picture.models import Picture, PictureInfo


class PictureListCreateSerializer(serializers.ModelSerializer):
    """
    Сериализатор для просмотра списка картинок и добавления
    """

    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(source='picture_information.name', read_only=True)
    width = serializers.IntegerField(source='picture_information.width', read_only=True)
    height = serializers.IntegerField(source='picture_information.height', read_only=True)
    parent_picture = serializers.IntegerField(source='picture_information.parent_picture.id',
                                              read_only=True, allow_null=True)

    class Meta:
        model = Picture
        fields = ('id', 'name', 'url', 'picture', 'width', 'height', 'parent_picture')

    def create(self, validated_data):
        # Открываем изображение чтобы считать его параметры
        picture_open = Image.open(validated_data.get('picture'))
        width = picture_open.width
        height = picture_open.height

        # Проверяем каким образом получена картинка через url или загрузку
        # Если был передан и url и картинка, но upload_from_url - False
        # (данная переменная необходима для понимания того, что загрузка произошла через url)
        # то сохраняется только картинка, url устанавливается в null
        if not self.initial_data.get('upload_from_url'):
            # если через загрузку, то создаем объект картинки, помещаем его в БД и создаем описание к ней
            obj_picture = Picture.objects.create(url=None, picture=validated_data.get('picture'))
            PictureInfo.objects.create(name=obj_picture.picture, picture_id=obj_picture.id,
                                       width=width, height=height, parent_picture_id=None)
            return obj_picture
        else:
            # еслич чере url, то создаем описание к картинке
            PictureInfo.objects.create(name=validated_data.get('picture'),
                                       picture_id=self.initial_data.get('picture_id'),
                                       width=width, height=height, parent_picture_id=None)
            a = PictureInfo.objects.get(name=validated_data.get('picture'))
            print(a.parent_picture)
            return Picture.objects.get(id=self.initial_data.get('picture_id'))


class PictureRetrieveDestroySerializer(serializers.ModelSerializer):
    """
    Сериализатор для просмотра конкретной картинки и удаления
    """

    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(source='picture_information.name', read_only=True)
    width = serializers.IntegerField(source='picture_information.width', read_only=True)
    height = serializers.IntegerField(source='picture_information.height', read_only=True)
    parent_picture = serializers.IntegerField(source='picture_information.parent_picture.id',
                                              read_only=True, allow_null=True)

    class Meta:
        model = Picture
        fields = ('id', 'name', 'url', 'picture', 'width', 'height', 'parent_picture')


class PictureResizeSerializer(serializers.ModelSerializer):
    """
    Сериализатор для изменения размеров конкретной картинки
    """

    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(source='picture_information.name', read_only=True)
    width = serializers.IntegerField(label='Ширина', source='picture_information.width',
                                     validators=[MinValueValidator(1), MaxValueValidator(10000)])
    height = serializers.IntegerField(label='Высота', source='picture_information.height',
                                      validators=[MinValueValidator(1), MaxValueValidator(10000)])
    parent_picture = serializers.IntegerField(source='picture_information.parent_picture.id', read_only=True)

    class Meta:
        model = Picture
        fields = '__all__'
        read_only_fields = ('id', 'name', 'url', 'picture', 'parent_picture')

    def create(self, validated_data):
        return self.initial_data.get('children_picture_id')

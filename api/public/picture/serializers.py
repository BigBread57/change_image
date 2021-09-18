from PIL import Image
from rest_framework import serializers

from picture.models import Picture, PictureInfo


class PictureListSerializer(serializers.ModelSerializer):
    """
    Сериализатор для просмотра списка картинок и добавления
    """

    id = serializers.IntegerField(source='picture_information.id')
    name = serializers.CharField(source='picture_information.name')
    width = serializers.IntegerField(source='picture_information.width')
    height = serializers.IntegerField(source='picture_information.height')
    parent_picture = serializers.IntegerField(source='picture_information.parent_picture')

    class Meta:
        model = Picture
        fields = ('id', 'name', 'url', 'picture', 'width', 'height', 'parent_picture')
        read_only_fields = fields


class PictureCreateSerializer(serializers.ModelSerializer):
    """
    Сериализатор для просмотра списка картинок и добавления
    """

    class Meta:
        model = Picture
        fields = '__all__'
        read_only_fields = ('id', 'name', 'width', 'height', 'parent_picture')


class PictureListCreateSerializer(serializers.ModelSerializer):
    """
    Сериализатор для просмотра списка картинок и добавления
    """

    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(source='picture_information.name', read_only=True)
    width = serializers.IntegerField(source='picture_information.width', read_only=True)
    height = serializers.IntegerField(source='picture_information.height', read_only=True)
    parent_picture = serializers.IntegerField(source='picture_information.parent_picture', read_only=True)

    class Meta:
        model = Picture
        fields = ('id', 'name', 'url', 'picture', 'width', 'height', 'parent_picture')

    def create(self, validated_data):
        # Открываем изображение чтобы считать его параметры
        picture_open = Image.open(validated_data.get('picture'))
        width = picture_open.width
        height = picture_open.height

        # Проверяем каким образом получена картинка через url или загрузку
        if not validated_data.get('url'):
            # если через загрузку, то создаем объект картинки, помещаем его в БД и создаем описание к ней
            obj_picture = Picture.objects.create(**validated_data)
            PictureInfo.objects.create(name=obj_picture.picture, picture_id=obj_picture.id,
                                       width=width, height=height)
            return obj_picture
        else:
            # еслич чере url, то создаем описание к картинке
            PictureInfo.objects.create(name=validated_data.get('picture'),
                                       picture_id=self.initial_data.get('picture_id'),
                                       width=width, height=height)
            return Picture.objects.get(id=self.initial_data.get('picture_id'))


class PictureRetrieveDestroySerializer(serializers.ModelSerializer):
    """
    Сериализатор для просмотра конкретной картинки и удаления
    """

    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(source='picture_information.name', read_only=True)
    width = serializers.IntegerField(source='picture_information.width', read_only=True)
    height = serializers.IntegerField(source='picture_information.height', read_only=True)
    parent_picture = serializers.IntegerField(source='picture_information.parent_picture', read_only=True)

    class Meta:
        model = Picture
        fields = ('id', 'name', 'url', 'picture', 'width', 'height', 'parent_picture')


class PictureResizeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Picture
        fields = '__all__'
        read_only_fields = ('id', 'name', 'url', 'picture', 'parent_picture')

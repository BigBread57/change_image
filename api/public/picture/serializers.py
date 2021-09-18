from rest_framework import serializers

from picture.models import Picture


class PictureListCreateSerializer(serializers.ModelSerializer):
    """
    Сериализатор для просмотра списка картинок и добавления
    """

    class Meta:
        model = Picture
        fields = '__all__'
        read_only_fields = ('id', 'name', 'width', 'height', 'parent_picture')


class PictureRetrieveDestroySerializer(serializers.ModelSerializer):
    """
    Сериализатор для просмотра конкретной картинки и удаления
    """

    class Meta:
        model = Picture
        fields = '__all__'


class PictureResizeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Picture
        fields = '__all__'
        read_only_fields = ('id', 'name', 'url', 'picture', 'parent_picture')

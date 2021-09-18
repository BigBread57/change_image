from rest_framework import serializers

from picture.models import Picture


class PictureListCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Picture
        fields = '__all__'

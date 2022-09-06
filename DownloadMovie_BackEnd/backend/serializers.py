from rest_framework import serializers
from .models import *


class SignUpSerializer(serializers.Serializer):
    # def create(self, validated_data):
    #     pass
    #
    # def update(self, instance, validated_data):
    #     pass

    first_name = serializers.CharField()
    last_name = serializers.CharField()
    email = serializers.EmailField()
    country = serializers.CharField()
    phone_number = serializers.CharField()
    username = serializers.CharField()
    password1 = serializers.CharField()
    password2 = serializers.CharField()


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('text',)


class FilmSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(read_only=True, many=True)

    class Meta:
        model = Film
        fields = ('id', 'name', 'summary', 'genre', 'director', 'actors', 'score', 'country',
                  'yearOfPublication', 'photo', 'comments')


class IdSerializer(serializers.Serializer):
    id = serializers.IntegerField()
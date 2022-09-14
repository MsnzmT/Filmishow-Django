from rest_framework import serializers
from .models import *


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('name', 'title')


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ('name', 'title')


class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = ('name', 'title')



class SignUpSerializer(serializers.Serializer):
    # def create(self, validated_data):
    #     pass
    #
    # def update(self, instance, validated_data):
    #     pass

    # first_name = serializers.CharField()
    # last_name = serializers.CharField()
    full_name = serializers.CharField()
    email = serializers.EmailField()
    # country = serializers.CharField()
    # phone_number = serializers.CharField()
    username = serializers.CharField()
    password1 = serializers.CharField()
    password2 = serializers.CharField()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('full_name', 'username')


class CommentSerializer(serializers.ModelSerializer):
    commenter = UserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ('id', 'text', 'date', 'commenter')


class FilmSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(read_only=True, many=True)
    genres = GenreSerializer(many=True, read_only=True)
    countries = CountrySerializer(many=True, read_only=True)
    language = LanguageSerializer(many=True, read_only=True)

    class Meta:
        model = Film
        fields = ('id', 'pName', 'eName', 'summary', 'genres', 'directors', 'actors', 'score', 'average_people', 'time',
                  'language', 'countries',
                  'yearOfPublication', 'photo', 'comments', 'group')


class IdSerializer(serializers.Serializer):
    id = serializers.IntegerField()


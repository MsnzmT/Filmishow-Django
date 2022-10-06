from rest_framework import serializers
from .models import *
from random import randint
from django.core.mail import send_mail
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


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
        fields = ('id', 'text', 'date', 'commenter', 'like', 'dislike')


class FilmSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(read_only=True, many=True)
    genres = GenreSerializer(many=True, read_only=True)
    countries = CountrySerializer(many=True, read_only=True)
    language = LanguageSerializer(many=True, read_only=True)

    class Meta:
        model = Film
        fields = ('id', 'pName', 'eName', 'summary', 'genres', 'directors', 'actors', 'score', 'average_people','like','dislike', 'time',
                  'language', 'countries',
                  'yearOfPublication', 'photo', 'comments', 'group', 'trailer', 'subtitle', 'poster', 'double', 'about')


class IdSerializer(serializers.Serializer):
    id = serializers.IntegerField()


class FilmSerializer2(serializers.ModelSerializer):
    class Meta:
        model = Film
        fields = ('id', 'eName', 'score', 'group', 'photo')


class ArrivalSerializer(serializers.ModelSerializer):
    film = FilmSerializer2(read_only=True)

    class Meta:
        model = ArrivalFilm
        fields = '__all__'


class EmailSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def create(self, validated_data):
        code = randint(100000, 1000000)
        send_mail('verification email', str(code), 'filmishow@mahdivakili.ir', [validated_data['email']])
        return EmailVerification.objects.create(email=validated_data['email'], token=code)


class EmailCodeSerializer(serializers.Serializer):
    email = serializers.EmailField()
    token = serializers.CharField()

    def validate(self, data):
        v = EmailVerification.objects.filter(email=data['email'], token=data['token'], is_verified=False)
        if not v.exists():
            raise serializers.ValidationError({'کد اشتباه است !'})
        return data

    def create(self, data):
        v = EmailVerification.objects.get(email=data['email'], token=data['token'])
        v.is_verified = True
        v.save()
        return v


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['full_name'] = user.last_name
        token['username'] = user.username
        token['is_superuser'] = user.is_superuser
        return token


class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = ('film_id', )

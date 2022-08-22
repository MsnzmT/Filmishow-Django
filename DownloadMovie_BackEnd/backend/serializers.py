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


class FilmSerializer(serializers.ModelSerializer):
    class Meta:
        model = Film
        fields = '__all__'


class AllFilmsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Film
        fields = ('name', 'photo')

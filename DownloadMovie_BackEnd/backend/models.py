from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
import jwt
from django.conf import settings


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    country = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    password = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    username = models.CharField(max_length=100, unique=True)


class Film(models.Model):
    GENRE_CHOICES = (('Horror', 'Horror'),
                     ('Drum', 'Drum'),
                     ('Action', 'Action'),
                     ('Comedy', 'Comedy'),
                     ('Fantasy', 'Fantasy'))
    # - - - - - Attributes - - - - -
    name = models.CharField(max_length=30)
    summary = models.TextField(max_length=200)
    genre = models.CharField(max_length=100, choices=GENRE_CHOICES)
    director = models.CharField(max_length=20)
    actors = models.CharField(max_length=500)
    score = models.FloatField(validators=[MinValueValidator(0.0), MaxValueValidator(10.0)])
    country = models.CharField(max_length=100)
    yearOfPublication = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(2022)])
    # photo = models.ImageField(null=True, blank=True, upload_to="MoviesPictures/")
    photo = models.CharField(max_length=800, null=True, blank=True)

    def __str__(self):
        return f'{self.name}'


class Comment(models.Model):
    commenter = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, related_name='commenter')
    film = models.ForeignKey(Film, on_delete=models.CASCADE, null=True, related_name='comments')
    text = models.TextField()
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.commenter} comments on {self.film}'

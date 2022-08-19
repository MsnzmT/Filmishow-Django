import datetime
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    country = models.CharField(max_length=20)
    phone_number = models.CharField(max_length=13)


class Film(models.Model):
    GENRE_CHOICES = (('H', 'Horror'),
                     ('D', 'Drum'),
                     ('A', 'Action'),
                     ('C', 'Comedy'),
                     ('F', 'Fantasy'))
    # - - - - - Attributes - - - - -
    name = models.CharField(max_length=30)
    summary = models.TextField(max_length=200)
    genre = models.CharField(max_length=1, choices=GENRE_CHOICES)
    director = models.CharField(max_length=20)
    actors = models.CharField(max_length=500)
    score = models.FloatField(validators=[MinValueValidator(0.0), MaxValueValidator(10.0)])
    country = models.CharField(max_length=100)
    yearOfPublication = models.DateField()
    photo = models.ImageField(null=True, blank=True)

    def __str__(self):
        return f'{self.name}'


class Comment(models.Model):
    commenter = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    film = models.ForeignKey(Film, on_delete=models.CASCADE, null=True)
    text = models.TextField()
    date = models.DateField(default=datetime.date.today(), null=True)

    def __str__(self):
        return f'{self.commenter} comments on {self.film}'

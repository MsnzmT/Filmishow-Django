from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    # country = models.CharField(max_length=100)
    # phone_number = models.CharField(max_length=20, blank=True, null=True)
    password = models.CharField(max_length=100)
    # first_name = models.CharField(max_length=100)
    # last_name = models.CharField(max_length=100)
    full_name = models.CharField(max_length=100, null=True)
    username = models.CharField(max_length=100, unique=True)


class Country(models.Model):
    name = models.CharField(max_length=100)
    title = models.CharField(max_length=100, null=True)

    def __str__(self):
        return f'{self.name}'


class Language(models.Model):
    name = models.CharField(max_length=100)
    title = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.name}'


class Genre(models.Model):
    GENRE_CHOICES = (('horror', 'horror'),
                     ('drum', 'drum'),
                     ('action', 'action'),
                     ('comedy', 'comedy'),
                     ('fantasy', 'fantasy'))

    name = models.CharField(choices=GENRE_CHOICES, max_length=20)
    title = models.CharField(max_length=20, null=True)

    def __str__(self):
        return f'{self.name}'


class Film(models.Model):
    GROUP_CHOICES = (
        ('Anime', 'Anime'),
        ('Animation', 'Animation'),
        ('Series', 'Series'),
        ('Movie', 'Movie')
    )
    # - - - - - Attributes - - - - -
    pName = models.CharField(max_length=30)
    eName = models.CharField(max_length=30, null=True)
    summary = models.TextField(max_length=200)
    genres = models.ManyToManyField(Genre, related_name='genres')
    directors = models.CharField(max_length=500)
    actors = models.CharField(max_length=500)
    score = models.FloatField(validators=[MinValueValidator(0.0), MaxValueValidator(10.0)])
    average_people = models.IntegerField(null=True)
    time = models.IntegerField(null=True)
    language = models.ManyToManyField(Language, related_name='language')
    countries = models.ManyToManyField(Country, related_name='countries')
    yearOfPublication = models.IntegerField(validators=[MinValueValidator(1000), MaxValueValidator(2022)])
    # photo = models.ImageField(null=True, blank=True, upload_to="MoviesPictures/")
    photo = models.CharField(max_length=800, null=True, blank=True)
    group = models.CharField(max_length=100, choices=GROUP_CHOICES, null=True)


    def __str__(self):
        return f'{self.eName}'


class Comment(models.Model):
    commenter = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, related_name='commenter')
    film = models.ForeignKey(Film, on_delete=models.CASCADE, null=True, related_name='comments')
    text = models.TextField()
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.commenter} comments on {self.film}'

from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.dispatch import receiver
from django.urls import reverse
from django_rest_passwordreset.signals import reset_password_token_created
from django.core.mail import send_mail


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
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
    summary = models.TextField(max_length=2000, null=True)
    about = models.TextField(max_length=2000, null=True)
    genres = models.ManyToManyField(Genre, related_name='genres')
    directors = models.CharField(max_length=500)
    actors = models.CharField(max_length=500)
    score = models.FloatField(validators=[MinValueValidator(0.0), MaxValueValidator(10.0)])
    average_people = models.IntegerField(null=True)
    like = models.IntegerField(null=True, default=0)
    dislike = models.IntegerField(null=True, default=0)
    time = models.IntegerField(null=True)
    language = models.ManyToManyField(Language, related_name='language')
    countries = models.ManyToManyField(Country, related_name='countries')
    yearOfPublication = models.IntegerField(validators=[MinValueValidator(1000), MaxValueValidator(2022)])
    # photo = models.ImageField(null=True, blank=True, upload_to="MoviesPictures/")
    photo = models.CharField(max_length=800, null=True, blank=True)
    trailer = models.CharField(max_length=800, null=True)
    poster = models.CharField(max_length=800, null=True)
    subtitle = models.BooleanField(null=True)
    double = models.BooleanField(null=True)
    group = models.CharField(max_length=100, choices=GROUP_CHOICES, null=True)

    def __str__(self):
        return f'{self.eName}'


class Comment(models.Model):
    commenter = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, related_name='commenter')
    film = models.ForeignKey(Film, on_delete=models.CASCADE, null=True, related_name='comments')
    text = models.TextField()
    date = models.DateTimeField(default=timezone.now)
    like = models.IntegerField(default=0, null=True)
    dislike = models.IntegerField(default=0, null=True)

    def __str__(self):
        return f'{self.commenter} comments on {self.film}'


class ArrivalFilm(models.Model):
    film = models.OneToOneField(Film, on_delete=models.CASCADE, related_name='film')

    def __str__(self):
        return f'{self.film.eName}'


class EmailVerification(models.Model):
    email = models.EmailField()
    token = models.CharField(max_length=200)
    is_verified = models.BooleanField(default=False)


class CommentLike(models.Model):
    comment_id = models.IntegerField()
    user_id = models.IntegerField()

    def __str__(self):
        return f'Comment_id : {self.comment_id} | User_id : {self.user_id}'


class CommentDislike(models.Model):
    comment_id = models.IntegerField()
    user_id = models.IntegerField()

    def __str__(self):
        return f'Comment_id : {self.comment_id} | User_id : {self.user_id}'


class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='user')
    favorites = models.ManyToManyField(Film,null=True)

    def __str__(self):
        return f'{self.user.username}'


@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):

    send_mail(
        # title:
        "Password Reset for {title}".format(title="Some website title"),
        # message:
        reset_password_token.key,
        # from:
        "filmishow@mahdivakili.ir",
        # to:
        [reset_password_token.user.email]
    )

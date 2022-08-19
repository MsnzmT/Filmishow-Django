from django.contrib import admin

# Register your models here.
from backend.models import Film, Comment, Profile


@admin.register(Film)
class FilmAdmin(admin.ModelAdmin):
    pass


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    pass


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    pass

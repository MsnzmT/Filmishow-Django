from django.contrib import admin
from backend.models import Film, Comment, Profile


class CommentInline(admin.StackedInline):
    model = Comment


@admin.register(Film)
class FilmAdmin(admin.ModelAdmin):
    inlines = [CommentInline]


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    pass


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    pass

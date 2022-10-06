from django.contrib import admin
from backend.models import *
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin


class CommentInline(admin.StackedInline):
    model = Comment


@admin.register(Film)
class FilmAdmin(admin.ModelAdmin):
    inlines = [CommentInline]


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name', 'title')


@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    list_display = ('name', 'title')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    pass


@admin.register(CustomUser)
class UserAdmin(DefaultUserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {
            'fields': (
                'full_name',
                'email',
            )
        }),
        ('Permissions', {
            'fields': (
                'is_active',
                'is_staff',
                'is_superuser',
                'groups',
                'user_permissions'
            ),
        }),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    list_display = (
        'username',
        'email',
        'full_name',
        'is_staff',
    )

    search_fields = (
        'username',
        'full_name',
        'phone_number',
        'email',
    )


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ('name', 'title')


@admin.register(ArrivalFilm)
class ArrivalAdmin(admin.ModelAdmin):
    pass


@admin.register(CommentLike)
class LikeAdmin(admin.ModelAdmin):
    pass


@admin.register(CommentDislike)
class DislikeAdmin(admin.ModelAdmin):
    pass


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    pass
from django.contrib import admin

# Register your models here.
from backend.models import Film


@admin.register(Film)
class film_admin(admin.ModelAdmin):
    pass
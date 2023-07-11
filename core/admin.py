from django.contrib import admin
from core.models import Url


@admin.register(Url)
class UrlAdmin(admin.ModelAdmin):
    list_display = ("id", "url", "hashed_url")

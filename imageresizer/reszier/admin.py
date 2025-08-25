from django.contrib import admin
from .models import ImageModel


@admin.register(ImageModel)
class ImageModelAdmin(admin.ModelAdmin):
    list_display = ('original_image', 'thumbnail_small', 'thumbnail_medium', 'thumbnail_large')

from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from PIL import Image
from django.core.files.base import ContentFile
import os
from io import BytesIO


class ImageModel(models.Model):
    original_image = models.ImageField(upload_to="images/")
    thumbnail_small = models.ImageField(upload_to="images/thumbnail", null=True, blank=True)
    thumbnail_medium = models.ImageField(upload_to="images/thumbnail", null=True, blank=True)
    thumbnail_large = models.ImageField(upload_to="images/thumbnail", null=True, blank=True)

    def __str__(self):
        return os.path.basename(self.original_image.name)

@receiver(post_save, sender=ImageModel)
def create_thumbnail(sender, instance, created, **kwargs):
    if created and instance.original_image:
        sizes = {
            'thumbnail_small': (100, 100),
            'thumbnail_medium': (300, 300),
            'thumbnail_large': (600, 600),
        }

        for field_name, size in sizes.items():
            img = Image.open(instance.original_image.path)
            img.thumbnail(size, Image.Resampling.LANCZOS)

            buffer = BytesIO()
            img_format = 'JPEG' if img.mode in ('RGB', 'L') else 'PNG'
            img.save(buffer, format=img_format)
            buffer.seek(0)

            file_name = f"{os.path.splitext(os.path.basename(instance.original_image.name))[0]}_{size[0]}x{size[1]}.{img_format.lower()}"
            django_file = ContentFile(buffer.read(), name=file_name)

            getattr(instance, field_name).save(file_name, django_file, save=False)

        instance.save()


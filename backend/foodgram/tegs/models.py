from django.db import models


class Tag(models.Model):
    name = models.CharField(
        unique=True,
        max_length=100,
    )
    color = models.CharField(
        unique=True,
        max_length=100,
    )
    slug = models.SlugField(
        unique=True,
    )

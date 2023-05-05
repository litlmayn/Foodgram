from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    first_name = models.CharField(
        'Имя',
        max_length=150,
    )
    last_name = models.CharField(
        'Фамилия',
        max_length=150,
    )
    email = models.EmailField(
        'email',
        max_length=254,
        unique=True,
    )
    password = models.CharField(
        max_length=150,
    )
    is_subscridet = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.username}'

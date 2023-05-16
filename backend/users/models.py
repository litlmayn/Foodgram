from django.contrib.auth.models import AbstractUser
from django.db import models

from api.constants import USER_MAX_LENGHT, EMAIL_MAX_LENGHT


class CustomUser(AbstractUser):
    username = models.CharField(
        max_length=USER_MAX_LENGHT, unique=True
    )
    first_name = models.CharField(
        'Имя',
        max_length=USER_MAX_LENGHT,
    )
    last_name = models.CharField(
        'Фамилия',
        max_length=USER_MAX_LENGHT,
    )
    email = models.EmailField(
        'email',
        max_length=EMAIL_MAX_LENGHT,
        unique=True,
    )
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'username', 'password']

    class Meta:
        ordering = ('username', 'first_name')
        verbose_name = 'Пользователь'

    def __str__(self):
        return f'{self.username}'

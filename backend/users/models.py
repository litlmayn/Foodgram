from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.db import models


class CustomUser(AbstractUser):
    username = models.CharField(
        max_length=settings.USER_MAX_LENGHT, unique=True
    )
    password = models.CharField(max_length=settings.USER_MAX_LENGHT)
    first_name = models.CharField(
        'Имя',
        max_length=settings.USER_MAX_LENGHT,
    )
    last_name = models.CharField(
        'Фамилия',
        max_length=settings.USER_MAX_LENGHT,
    )
    email = models.EmailField(
        'email',
        max_length=settings.EMAIL_MAX_LENGHT,
        unique=True,
    )
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'username', 'password']

    class Meta:
        ordering = ('id',)
        verbose_name = 'Пользователь'

    def __str__(self):
        return f'{self.username}'

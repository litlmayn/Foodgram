from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    USER = 'user'
    ADMIN = 'admin'
    ROLE_CHOICES = [
        (USER, 'Пользователь'),
        (ADMIN, 'Администратор'),
    ]
    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=254)
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
    role = models.CharField(
        'Роль пользователя',
        max_length=max(len(role) for role, _ in ROLE_CHOICES),
        choices=ROLE_CHOICES,
        default=USER,
    )
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'username', 'password']

    class Meta:
        ordering = ('id',)
        verbose_name = 'Пользователь'

    @property
    def is_admin(self):
        return (
                self.role == 'admin'
                or self.is_superuser
        )

    def __str__(self):
        return f'{self.username}'

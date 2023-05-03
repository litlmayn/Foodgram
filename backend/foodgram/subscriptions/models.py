from django.db import models


class Subscription(models.Model):
    user = models.ForeignKey(
        'users.CustomUser',
        on_delete=models.CASCADE,
        related_name='follower',
    )
    following = models.ForeignKey(
        'users.CustomUser',
        on_delete=models.CASCADE,
        related_name='following',
    )

    def __str__(self):
        return f'{self.user}, {self.following}'

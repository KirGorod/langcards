from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class SiteComment(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='site_comments'
    )
    message = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.user.username} Site Comment'

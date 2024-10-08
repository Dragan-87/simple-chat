from django.db import models
from datetime import date
from django.conf import settings



class Chat(models.Model):
    created_at = models.DateField(default=date.today)


class Message(models.Model):
    text = models.CharField(max_length=500)
    created_at = models.DateField(default=date.today)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='author_message_set')
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='receiver_message_set')
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, default=None, blank=True, null=True)


from django.contrib.auth.models import User
from django.db import models
from django.conf import settings


class ChatHistory(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    prompt = models.TextField(max_length=500)
    response = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
from django.db import models
from users.models import User

class ChatHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    prompt = models.CharField(max_length=512)
    response = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

from django.contrib import admin
from .models import User, ChatHistory  # Import User and ChatHistory models

# Register your models here.
admin.site.register(User)
admin.site.register(ChatHistory)  # Register ChatHistory with the admin

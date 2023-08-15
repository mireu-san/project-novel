from rest_framework import serializers
from .models import ChatHistory


class ChatHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatHistory
        # fields = ('id', 'user', 'prompt', 'response', 'timestamp')
        fields = '__all__'
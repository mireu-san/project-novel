# from django.shortcuts import render
from rest_framework import generics
from .models import ChatHistory
from .serializers import ChatHistorySerializer


class ChatHistoryCreateView(generics.CreateAPIView):
    queryset = ChatHistory.objects.all()
    serializer_class = ChatHistorySerializer

    def perform_create(self, serializer):
        # Assign the authenticated user to the user field
        serializer.save(user=self.request.user)


class UserChatHistoryListView(generics.ListAPIView):
    serializer_class = ChatHistorySerializer

    def get_queryset(self):
        # Filter chat history records by the authenticated user
        return ChatHistory.objects.filter(user=self.request.user)

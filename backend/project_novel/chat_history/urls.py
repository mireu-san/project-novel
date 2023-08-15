from django.urls import path
from .views import ChatHistoryCreateView, UserChatHistoryListView

urlpatterns = [
    path('chat-history/', ChatHistoryCreateView.as_view(), name='chat-history-create'),
    path('user-chat-history/', UserChatHistoryListView.as_view(), name='user-chat-history-list'),
]

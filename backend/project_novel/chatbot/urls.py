# You are viewing a ★chatbot/urls.py

from django.urls import path, include
from .views import ChatbotView, ConversationViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'conversation', ConversationViewSet)

urlpatterns = [
	path('', ChatbotView.as_view(), name='chat'),
    path('api/', include(router.urls)),
]
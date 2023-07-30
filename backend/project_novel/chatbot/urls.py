# ★chatbot/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ChatbotView, ConversationViewSet

routers = DefaultRouter()
routers.register(r'conversation', ConversationViewSet)

urlpatterns = [
    path('api/chat/', ChatbotView.as_view(), name='chatbot'),
    # ConversationViewSet 에서 정의한 url 을 사용하기 위해 routers.urls 를 사용
    path('api/', include(routers.urls))
]

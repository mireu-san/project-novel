# ★chatbot/urls.py
from django.urls import path, include

# from rest_framework.routers import DefaultRouter
from .views import ChatbotView, ConversationView, TaskResultView

# routers = DefaultRouter()
# routers.register(r'conversation', ConversationViewSet)

urlpatterns = [
    # 실시간 채팅 상호작용에 중점. 사용자 입력 처리 및 AI 응답 생성 담당.
    path("api/chat/", ChatbotView.as_view(), name="chatbot"),
    path("api/conversation/", ConversationView.as_view(), name="conversation"),
    path("task-result/<str:task_id>/", TaskResultView.as_view(), name="task_result"),
    # ConversationViewSet 에서 정의한 url 을 사용하기 위해 routers.urls 를 사용
    # 대화 데이터를 관리하기 위한 CRUD 작업 세트를 제공
    # path('api/', include(routers.urls))
]
